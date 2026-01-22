# AWS Infrastructure Deployment Guide

## Prerequisites

1. **AWS CLI installed and configured**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```

2. **Required AWS permissions**
   - CloudFormation full access
   - EC2 full access
   - ECS full access
   - RDS full access
   - ECR full access
   - IAM role creation

## Deployment Steps

### 1. Create Database Password Secret

```bash
# Create a secure password for the database
aws secretsmanager create-secret \
    --name "content-aggregator-prod-db-password" \
    --description "Database password for Content Aggregator production" \
    --secret-string '{"password":"YOUR_SECURE_PASSWORD_HERE"}'
```

### 2. Deploy Infrastructure

```bash
# Deploy the CloudFormation stack
aws cloudformation create-stack \
    --stack-name content-aggregator-prod \
    --template-body file://infrastructure/aws-resources.yml \
    --parameters ParameterKey=ProjectName,ParameterValue=content-aggregator \
                 ParameterKey=Environment,ParameterValue=prod \
    --capabilities CAPABILITY_IAM
```

### 3. Wait for Stack Creation

```bash
# Monitor stack creation
aws cloudformation wait stack-create-complete \
    --stack-name content-aggregator-prod

# Get stack outputs
aws cloudformation describe-stacks \
    --stack-name content-aggregator-prod \
    --query 'Stacks[0].Outputs'
```

### 4. Configure ECR Repository

```bash
# Get ECR login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ECR_URI>

# Build and push Docker image
cd backend
docker build -t content-aggregator-prod .
docker tag content-aggregator-prod:latest <ECR_URI>:latest
docker push <ECR_URI>:latest
```

### 5. Create ECS Task Definition and Service

This will be handled by the CI/CD pipeline in Phase 2.

## Infrastructure Components

- **VPC**: Isolated network with public and private subnets
- **ECS Cluster**: Fargate cluster for running containers
- **RDS**: PostgreSQL database in private subnets
- **ECR**: Container registry for Docker images
- **ALB**: Application Load Balancer for traffic distribution
- **Security Groups**: Network access controls

## Outputs

After successful deployment, you'll have:
- ECR Repository URI for pushing Docker images
- ECS Cluster name for service deployment
- RDS endpoint for database connections
- ALB ARN for load balancer configuration

## Cleanup

To delete all resources:

```bash
aws cloudformation delete-stack --stack-name content-aggregator-prod
```

## Troubleshooting

1. **Stack creation fails**: Check CloudFormation events in AWS Console
2. **RDS creation timeout**: Database creation can take 10-15 minutes
3. **Permission errors**: Ensure your AWS user has required permissions
4. **Secret not found**: Verify the database password secret was created
