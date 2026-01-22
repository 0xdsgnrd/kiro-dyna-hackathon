# CI/CD Pipeline Setup Guide

## Overview

This guide sets up automated deployment pipelines for both frontend and backend components using GitHub Actions, AWS ECS, and Vercel.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Vercel Account** connected to GitHub
3. **GitHub Repository** with Actions enabled
4. **Infrastructure deployed** (Phase 1 complete)

## Setup Steps

### 1. AWS ECS Service Setup

After deploying the CloudFormation stack, run the ECS setup script:

```bash
cd infrastructure
./setup-ecs-service.sh
```

This script will:
- Create CloudWatch log groups
- Set up IAM roles for ECS tasks
- Create secrets in AWS Secrets Manager
- Register the ECS task definition
- Create the ECS service

### 2. GitHub Secrets Configuration

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

**AWS Secrets:**
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key

**Vercel Secrets:**
- `VERCEL_TOKEN` - Vercel deployment token
- `VERCEL_ORG_ID` - Your Vercel organization ID
- `VERCEL_PROJECT_ID` - Your Vercel project ID
- `NEXT_PUBLIC_API_URL` - Your API endpoint URL

### 3. Vercel Project Setup

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login and link project:**
   ```bash
   cd frontend
   vercel login
   vercel link
   ```

3. **Get project information:**
   ```bash
   vercel project ls
   ```

4. **Set environment variables in Vercel dashboard**

### 4. Test the Pipeline

1. **Make a change to backend code**
2. **Commit and push to main branch**
3. **Check GitHub Actions tab for deployment progress**
4. **Verify deployment in AWS ECS console**

## Pipeline Features

### Backend Pipeline (`deploy-backend.yml`)
- **Testing**: Runs pytest with coverage reporting
- **Building**: Creates Docker image and pushes to ECR
- **Deployment**: Updates ECS service with new image
- **Migration**: Runs database migrations automatically
- **Monitoring**: Waits for service stability

### Frontend Pipeline (`deploy-frontend.yml`)
- **Testing**: Runs linting and Jest tests
- **Building**: Creates optimized Next.js build
- **Deployment**: Deploys to Vercel with production configuration
- **CDN**: Automatic CDN distribution and caching

## Deployment Flow

```
Code Push → GitHub Actions → Tests → Build → Deploy → Health Check
```

### Backend Flow:
1. Code pushed to `main` branch
2. Tests run with coverage reporting
3. Docker image built and pushed to ECR
4. ECS task definition updated
5. ECS service updated with zero-downtime deployment
6. Database migrations run automatically
7. Health checks verify deployment success

### Frontend Flow:
1. Code pushed to `main` branch
2. Linting and tests run
3. Next.js application built
4. Deployed to Vercel with CDN
5. Environment variables applied
6. Preview URL generated

## Monitoring and Rollback

### Health Checks
- Backend: `/health` endpoint monitored
- Frontend: Vercel automatic health monitoring
- ECS: Container health checks configured

### Rollback Procedure
```bash
# Backend rollback
aws ecs update-service \
  --cluster content-aggregator-prod \
  --service content-aggregator-service \
  --task-definition content-aggregator-task:PREVIOUS_REVISION

# Frontend rollback (via Vercel dashboard or CLI)
vercel rollback
```

## Troubleshooting

### Common Issues

1. **ECS Task Fails to Start**
   - Check CloudWatch logs: `/ecs/content-aggregator-prod`
   - Verify secrets are correctly configured
   - Check security group rules

2. **Database Connection Issues**
   - Verify RDS endpoint in secrets
   - Check security group allows ECS access
   - Confirm database credentials

3. **Vercel Deployment Fails**
   - Check build logs in Vercel dashboard
   - Verify environment variables
   - Check Next.js configuration

4. **GitHub Actions Fails**
   - Check Actions tab for detailed logs
   - Verify all secrets are configured
   - Check AWS permissions

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster content-aggregator-prod --services content-aggregator-service

# View ECS logs
aws logs tail /ecs/content-aggregator-prod --follow

# Check ECR images
aws ecr describe-images --repository-name content-aggregator-prod

# Test API endpoint
curl -f https://your-api-domain.com/health
```

## Security Considerations

- All secrets stored in AWS Secrets Manager or GitHub Secrets
- ECS tasks run with least-privilege IAM roles
- VPC security groups restrict network access
- HTTPS enforced for all endpoints
- Container images scanned for vulnerabilities

## Performance Optimization

- Docker image layers optimized for caching
- ECS tasks use Fargate for serverless scaling
- Vercel CDN for global frontend distribution
- Database connection pooling configured
- Health checks prevent traffic to unhealthy instances
