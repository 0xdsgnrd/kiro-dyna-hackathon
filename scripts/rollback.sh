#!/bin/bash

# Rollback procedure for production deployment
# Provides safe rollback mechanisms for failed deployments

set -e

PROJECT_NAME="content-aggregator"
ENVIRONMENT="prod"
AWS_REGION="us-east-1"

echo "🔄 Production Rollback Procedure"
echo "================================"

show_help() {
    echo "Usage: $0 <rollback_type> [options]"
    echo ""
    echo "Rollback Types:"
    echo "  ecs-service     - Rollback ECS service to previous task definition"
    echo "  database        - Rollback database to previous backup"
    echo "  frontend        - Rollback frontend deployment (Vercel)"
    echo "  full            - Full system rollback (all components)"
    echo ""
    echo "Options:"
    echo "  --revision N    - Specific revision to rollback to (for ECS)"
    echo "  --backup-id ID  - Specific backup to restore (for database)"
    echo "  --confirm       - Skip confirmation prompts"
    echo ""
    echo "Examples:"
    echo "  $0 ecs-service --revision 5"
    echo "  $0 database --backup-id db-backup-20260120"
    echo "  $0 full --confirm"
}

confirm_action() {
    local action="$1"
    if [[ "$CONFIRM" != "true" ]]; then
        echo "⚠️  WARNING: About to perform rollback: $action"
        read -p "Are you sure? (yes/no): " -r
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            echo "Rollback cancelled."
            exit 1
        fi
    fi
}

rollback_ecs_service() {
    local revision="$1"
    
    echo "🔄 Rolling back ECS service..."
    
    # Get current task definition
    CURRENT_TASK_DEF=$(aws ecs describe-services \
        --cluster "${PROJECT_NAME}-${ENVIRONMENT}" \
        --services "${PROJECT_NAME}-service" \
        --query 'services[0].taskDefinition' \
        --output text)
    
    echo "Current task definition: $CURRENT_TASK_DEF"
    
    # Determine target revision
    if [[ -n "$revision" ]]; then
        TARGET_TASK_DEF="${PROJECT_NAME}-task:$revision"
    else
        # Get previous revision
        CURRENT_REV=$(echo "$CURRENT_TASK_DEF" | cut -d':' -f2)
        PREV_REV=$((CURRENT_REV - 1))
        TARGET_TASK_DEF="${PROJECT_NAME}-task:$PREV_REV"
    fi
    
    echo "Target task definition: $TARGET_TASK_DEF"
    
    confirm_action "ECS service rollback to $TARGET_TASK_DEF"
    
    # Update service
    aws ecs update-service \
        --cluster "${PROJECT_NAME}-${ENVIRONMENT}" \
        --service "${PROJECT_NAME}-service" \
        --task-definition "$TARGET_TASK_DEF"
    
    echo "✅ ECS service rollback initiated"
    echo "⏳ Waiting for service to stabilize..."
    
    aws ecs wait services-stable \
        --cluster "${PROJECT_NAME}-${ENVIRONMENT}" \
        --services "${PROJECT_NAME}-service"
    
    echo "✅ ECS service rollback completed"
}

rollback_database() {
    local backup_id="$1"
    
    echo "🔄 Rolling back database..."
    
    # List available backups if no backup_id provided
    if [[ -z "$backup_id" ]]; then
        echo "Available database snapshots:"
        aws rds describe-db-snapshots \
            --db-instance-identifier "${PROJECT_NAME}-${ENVIRONMENT}-db" \
            --query 'DBSnapshots[?Status==`available`].[DBSnapshotIdentifier,SnapshotCreateTime]' \
            --output table
        
        read -p "Enter snapshot identifier to restore: " backup_id
    fi
    
    confirm_action "Database rollback to snapshot $backup_id"
    
    # Create a new DB instance from snapshot
    NEW_DB_ID="${PROJECT_NAME}-${ENVIRONMENT}-db-restored-$(date +%Y%m%d%H%M%S)"
    
    echo "Creating new database instance from snapshot..."
    aws rds restore-db-instance-from-db-snapshot \
        --db-instance-identifier "$NEW_DB_ID" \
        --db-snapshot-identifier "$backup_id" \
        --db-instance-class db.t3.micro
    
    echo "⏳ Waiting for database restore to complete..."
    aws rds wait db-instance-available --db-instance-identifier "$NEW_DB_ID"
    
    echo "✅ Database restored to new instance: $NEW_DB_ID"
    echo "⚠️  Manual step required: Update application configuration to use new database endpoint"
    
    # Get new endpoint
    NEW_ENDPOINT=$(aws rds describe-db-instances \
        --db-instance-identifier "$NEW_DB_ID" \
        --query 'DBInstances[0].Endpoint.Address' \
        --output text)
    
    echo "New database endpoint: $NEW_ENDPOINT"
}

rollback_frontend() {
    echo "🔄 Rolling back frontend deployment..."
    
    confirm_action "Frontend rollback via Vercel"
    
    # Check if Vercel CLI is available
    if command -v vercel &> /dev/null; then
        echo "Using Vercel CLI for rollback..."
        cd frontend
        vercel rollback
        cd ..
    else
        echo "⚠️  Vercel CLI not found. Manual rollback required:"
        echo "1. Go to Vercel dashboard"
        echo "2. Select your project"
        echo "3. Go to Deployments tab"
        echo "4. Click 'Promote to Production' on a previous deployment"
    fi
    
    echo "✅ Frontend rollback completed"
}

rollback_full() {
    echo "🔄 Performing full system rollback..."
    
    confirm_action "Full system rollback (ECS + Database + Frontend)"
    
    echo "Step 1: Rolling back ECS service..."
    rollback_ecs_service
    
    echo "Step 2: Rolling back database..."
    rollback_database
    
    echo "Step 3: Rolling back frontend..."
    rollback_frontend
    
    echo "✅ Full system rollback completed"
    echo "⚠️  Please verify all systems are working correctly"
}

# Parse command line arguments
ROLLBACK_TYPE=""
REVISION=""
BACKUP_ID=""
CONFIRM="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        ecs-service|database|frontend|full)
            ROLLBACK_TYPE="$1"
            shift
            ;;
        --revision)
            REVISION="$2"
            shift 2
            ;;
        --backup-id)
            BACKUP_ID="$2"
            shift 2
            ;;
        --confirm)
            CONFIRM="true"
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$ROLLBACK_TYPE" ]]; then
    echo "Error: Rollback type is required"
    show_help
    exit 1
fi

# Execute rollback based on type
case $ROLLBACK_TYPE in
    ecs-service)
        rollback_ecs_service "$REVISION"
        ;;
    database)
        rollback_database "$BACKUP_ID"
        ;;
    frontend)
        rollback_frontend
        ;;
    full)
        rollback_full
        ;;
    *)
        echo "Error: Invalid rollback type: $ROLLBACK_TYPE"
        show_help
        exit 1
        ;;
esac

echo ""
echo "🎉 Rollback procedure completed!"
echo "📋 Next steps:"
echo "   1. Verify application functionality"
echo "   2. Check monitoring dashboards"
echo "   3. Notify stakeholders of rollback"
echo "   4. Investigate root cause of original issue"
