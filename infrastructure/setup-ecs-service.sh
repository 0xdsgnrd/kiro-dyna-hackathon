#!/bin/bash

# ECS Service and Task Definition Setup Script
# Run this after CloudFormation stack is created

set -e

# Configuration
PROJECT_NAME="content-aggregator"
ENVIRONMENT="prod"
AWS_REGION="us-east-1"
CLUSTER_NAME="${PROJECT_NAME}-${ENVIRONMENT}"
SERVICE_NAME="${PROJECT_NAME}-service"
TASK_FAMILY="${PROJECT_NAME}-task"

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Setting up ECS service for account: $ACCOUNT_ID"

# Create CloudWatch Log Group
aws logs create-log-group \
    --log-group-name "/ecs/${PROJECT_NAME}-${ENVIRONMENT}" \
    --region $AWS_REGION || echo "Log group already exists"

# Create ECS Task Execution Role
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://trust-policy.json || echo "Role already exists"

aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# Create secrets in AWS Secrets Manager
aws secretsmanager create-secret \
    --name "${PROJECT_NAME}-${ENVIRONMENT}-secret-key" \
    --description "JWT secret key for ${PROJECT_NAME}" \
    --secret-string "$(openssl rand -base64 32)" || echo "Secret already exists"

# Get RDS endpoint from CloudFormation
RDS_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
    --query 'Stacks[0].Outputs[?OutputKey==`RDSEndpoint`].OutputValue' \
    --output text)

# Create database URL secret
DB_PASSWORD=$(aws secretsmanager get-secret-value \
    --secret-id "${PROJECT_NAME}-${ENVIRONMENT}-db-password" \
    --query SecretString --output text | jq -r .password)

DATABASE_URL="postgresql://postgres:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/contentdb"

aws secretsmanager create-secret \
    --name "${PROJECT_NAME}-${ENVIRONMENT}-database-url" \
    --description "Database URL for ${PROJECT_NAME}" \
    --secret-string "$DATABASE_URL" || \
aws secretsmanager update-secret \
    --secret-id "${PROJECT_NAME}-${ENVIRONMENT}-database-url" \
    --secret-string "$DATABASE_URL"

# Update task definition with actual account ID
sed "s/ACCOUNT_ID/$ACCOUNT_ID/g" infrastructure/ecs-task-definition.json > task-definition-updated.json

# Register task definition
aws ecs register-task-definition \
    --cli-input-json file://task-definition-updated.json

# Get VPC and subnet information from CloudFormation
VPC_ID=$(aws cloudformation describe-stacks \
    --stack-name "${PROJECT_NAME}-${ENVIRONMENT}" \
    --query 'Stacks[0].Outputs[?OutputKey==`VPCId`].OutputValue' \
    --output text)

SUBNET_IDS=$(aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=tag:Name,Values=*public*" \
    --query 'Subnets[].SubnetId' \
    --output text | tr '\t' ',')

SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=${PROJECT_NAME}-${ENVIRONMENT}-ecs-sg" \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

# Create ECS service
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition $TASK_FAMILY \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}" \
    --enable-execute-command || echo "Service already exists"

echo "ECS service setup complete!"
echo "Service: $SERVICE_NAME"
echo "Cluster: $CLUSTER_NAME"
echo "Task Definition: $TASK_FAMILY"

# Cleanup
rm -f trust-policy.json task-definition-updated.json
