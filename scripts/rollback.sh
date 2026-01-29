#!/bin/bash

# Content Aggregator Platform - Rollback Script
# This script rolls back the application to a previous version

set -e

# Configuration
ENVIRONMENT=${1:-prod}
TARGET_VERSION=${2}
AWS_REGION=${AWS_REGION:-us-east-1}
ECS_CLUSTER="content-aggregator-${ENVIRONMENT}"
ECS_SERVICE="content-aggregator-service"

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

# Show usage
usage() {
    echo "Usage: $0 [environment] [target_version]"
    echo "  environment: prod, staging, dev (default: prod)"
    echo "  target_version: specific version to rollback to (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 prod                    # Rollback to previous version"
    echo "  $0 prod abc123             # Rollback to specific version"
    exit 1
}

# List available versions
list_versions() {
    log "Available task definition versions:"
    
    aws ecs list-task-definitions \
        --family-prefix content-aggregator-${ENVIRONMENT} \
        --status ACTIVE \
        --sort DESC \
        --query 'taskDefinitionArns[0:10]' \
        --output table
}

# Get current deployment info
get_current_deployment() {
    log "Getting current deployment information..."
    
    CURRENT_TASK_DEF=$(aws ecs describe-services \
        --cluster $ECS_CLUSTER \
        --services $ECS_SERVICE \
        --query 'services[0].taskDefinition' \
        --output text)
    
    CURRENT_VERSION=$(echo $CURRENT_TASK_DEF | grep -o '[0-9]*$')
    
    log "Current task definition: $CURRENT_TASK_DEF"
    log "Current version: $CURRENT_VERSION"
}

# Get target version
get_target_version() {
    if [ -z "$TARGET_VERSION" ]; then
        # Get previous version (current - 1)
        TARGET_VERSION=$((CURRENT_VERSION - 1))
        log "No target version specified, using previous version: $TARGET_VERSION"
    fi
    
    TARGET_TASK_DEF="arn:aws:ecs:${AWS_REGION}:$(aws sts get-caller-identity --query Account --output text):task-definition/content-aggregator-${ENVIRONMENT}:${TARGET_VERSION}"
    
    # Verify target version exists
    if ! aws ecs describe-task-definition \
        --task-definition $TARGET_TASK_DEF &> /dev/null; then
        error "Target task definition does not exist: $TARGET_TASK_DEF"
    fi
    
    log "Target task definition: $TARGET_TASK_DEF"
}

# Perform rollback
perform_rollback() {
    log "Starting rollback to version $TARGET_VERSION..."
    
    # Confirm rollback
    read -p "Are you sure you want to rollback from version $CURRENT_VERSION to $TARGET_VERSION? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Rollback cancelled"
        exit 0
    fi
    
    # Update service with target task definition
    log "Updating ECS service..."
    aws ecs update-service \
        --cluster $ECS_CLUSTER \
        --service $ECS_SERVICE \
        --task-definition $TARGET_TASK_DEF \
        --force-new-deployment
    
    log "Waiting for service to stabilize..."
    aws ecs wait services-stable \
        --cluster $ECS_CLUSTER \
        --services $ECS_SERVICE
    
    log "Rollback completed successfully"
}

# Health check after rollback
health_check() {
    log "Performing health check..."
    
    # Get load balancer DNS
    ALB_DNS=$(aws cloudformation describe-stacks \
        --stack-name content-aggregator-${ENVIRONMENT} \
        --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
        --output text)
    
    local max_attempts=20
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

# Emergency rollback (skip confirmations)
emergency_rollback() {
    log "EMERGENCY ROLLBACK MODE - Skipping confirmations"
    
    get_current_deployment
    get_target_version
    
    log "Emergency rollback to version $TARGET_VERSION..."
    aws ecs update-service \
        --cluster $ECS_CLUSTER \
        --service $ECS_SERVICE \
        --task-definition $TARGET_TASK_DEF \
        --force-new-deployment
    
    log "Emergency rollback initiated"
}

# Main function
main() {
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        usage
    fi
    
    if [ "$1" = "--emergency" ]; then
        emergency_rollback
        exit 0
    fi
    
    if [ "$1" = "--list" ]; then
        list_versions
        exit 0
    fi
    
    log "Starting rollback process for environment: $ENVIRONMENT"
    
    get_current_deployment
    get_target_version
    perform_rollback
    health_check
    
    log "Rollback completed successfully!"
    log "Current version is now: $TARGET_VERSION"
}

# Run main function
main "$@"
