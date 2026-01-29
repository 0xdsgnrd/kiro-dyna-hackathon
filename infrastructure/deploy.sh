#!/bin/bash

# Content Aggregator Platform - AWS Deployment Script
# This script deploys the infrastructure and application to AWS

set -e

# Configuration
ENVIRONMENT=${1:-prod}
AWS_REGION=${AWS_REGION:-us-east-1}
STACK_NAME="content-aggregator-${ENVIRONMENT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured"
    fi
    
    log "Prerequisites check passed"
}

# Deploy CloudFormation stack
deploy_infrastructure() {
    log "Deploying infrastructure stack..."
    
    # Check if stack exists
    if aws cloudformation describe-stacks --stack-name $STACK_NAME &> /dev/null; then
        log "Updating existing stack: $STACK_NAME"
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://infrastructure/cloudformation-stack.yml \
            --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
            --capabilities CAPABILITY_IAM
    else
        log "Creating new stack: $STACK_NAME"
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://infrastructure/cloudformation-stack.yml \
            --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
            --capabilities CAPABILITY_IAM
    fi
    
    log "Waiting for stack deployment to complete..."
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME || \
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
    
    log "Infrastructure deployment completed"
}

# Get stack outputs
get_stack_outputs() {
    log "Retrieving stack outputs..."
    
    ECR_URI=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ECRRepositoryURI`].OutputValue' \
        --output text)
    
    ECS_CLUSTER=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`ECSClusterName`].OutputValue' \
        --output text)
    
    ALB_DNS=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
        --output text)
    
    log "ECR Repository: $ECR_URI"
    log "ECS Cluster: $ECS_CLUSTER"
    log "Load Balancer: $ALB_DNS"
}

# Build and push Docker image
build_and_push_image() {
    log "Building and pushing Docker image..."
    
    # Login to ECR
    aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin $ECR_URI
    
    # Build image
    cd backend
    docker build -t content-aggregator:latest .
    docker tag content-aggregator:latest $ECR_URI:latest
    docker tag content-aggregator:latest $ECR_URI:$(git rev-parse --short HEAD)
    
    # Push image
    docker push $ECR_URI:latest
    docker push $ECR_URI:$(git rev-parse --short HEAD)
    
    cd ..
    log "Docker image pushed successfully"
}

# Create ECS service
create_ecs_service() {
    log "Creating/updating ECS service..."
    
    # Update task definition with actual ECR URI
    sed "s|ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/content-aggregator-prod|$ECR_URI|g" \
        infrastructure/ecs-task-definition.json > /tmp/task-definition.json
    
    # Register task definition
    TASK_DEFINITION_ARN=$(aws ecs register-task-definition \
        --cli-input-json file:///tmp/task-definition.json \
        --query 'taskDefinition.taskDefinitionArn' \
        --output text)
    
    log "Registered task definition: $TASK_DEFINITION_ARN"
    
    # Check if service exists
    if aws ecs describe-services \
        --cluster $ECS_CLUSTER \
        --services content-aggregator-service &> /dev/null; then
        
        log "Updating existing ECS service..."
        aws ecs update-service \
            --cluster $ECS_CLUSTER \
            --service content-aggregator-service \
            --task-definition $TASK_DEFINITION_ARN \
            --force-new-deployment
    else
        log "Creating new ECS service..."
        aws ecs create-service \
            --cluster $ECS_CLUSTER \
            --service-name content-aggregator-service \
            --task-definition $TASK_DEFINITION_ARN \
            --desired-count 2 \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
            --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:$AWS_REGION:xxx:targetgroup/xxx,containerName=content-aggregator,containerPort=8000"
    fi
    
    log "Waiting for service to stabilize..."
    aws ecs wait services-stable \
        --cluster $ECS_CLUSTER \
        --services content-aggregator-service
    
    log "ECS service deployment completed"
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."
    
    aws ecs run-task \
        --cluster $ECS_CLUSTER \
        --task-definition content-aggregator-prod \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
        --overrides '{
            "containerOverrides": [{
                "name": "content-aggregator",
                "command": ["python", "-m", "app.db.migrate"]
            }]
        }' \
        --wait
    
    log "Database migrations completed"
}

# Health check
health_check() {
    log "Performing health check..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "http://$ALB_DNS/health" &> /dev/null; then
            log "Health check passed!"
            return 0
        fi
        
        log "Health check attempt $attempt/$max_attempts failed, retrying in 10s..."
        sleep 10
        ((attempt++))
    done
    
    error "Health check failed after $max_attempts attempts"
}

# Main deployment function
main() {
    log "Starting deployment for environment: $ENVIRONMENT"
    
    check_prerequisites
    deploy_infrastructure
    get_stack_outputs
    build_and_push_image
    create_ecs_service
    run_migrations
    health_check
    
    log "Deployment completed successfully!"
    log "Application URL: http://$ALB_DNS"
}

# Run main function
main "$@"
