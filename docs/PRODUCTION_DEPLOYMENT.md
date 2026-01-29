# Production Deployment Guide

## Overview

This guide covers the complete production deployment of the Content Aggregation Platform to AWS using Infrastructure as Code (CloudFormation) and automated CI/CD pipelines.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vercel CDN    │    │  Application     │    │   Amazon RDS    │
│   (Frontend)    │◄──►│  Load Balancer   │◄──►│  (PostgreSQL)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   ECS Fargate    │
                       │   (Backend API)  │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  CloudWatch      │
                       │  (Monitoring)    │
                       └──────────────────┘
```

## Prerequisites

### Required Tools
- AWS CLI v2.x
- Docker 20.x+
- Node.js 18+
- Python 3.11+
- Git

### AWS Account Setup
1. **IAM User with Permissions:**
   ```bash
   # Required AWS permissions
   - AmazonECS_FullAccess
   - AmazonEC2ContainerRegistryFullAccess
   - AmazonRDSFullAccess
   - CloudFormationFullAccess
   - AmazonVPCFullAccess
   - ElasticLoadBalancingFullAccess
   - CloudWatchFullAccess
   - SecretsManagerFullAccess
   ```

2. **Configure AWS CLI:**
   ```bash
   aws configure
   # Enter your Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)
   ```

### Environment Variables
Create the following secrets in your CI/CD system:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Vercel (for frontend)
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id

# Application URLs
NEXT_PUBLIC_API_URL=https://your-alb-dns.us-east-1.elb.amazonaws.com/api/v1
BACKEND_URL=https://your-alb-dns.us-east-1.elb.amazonaws.com
FRONTEND_URL=https://your-app.vercel.app
```

## Deployment Process

### 1. Infrastructure Deployment

Deploy the core infrastructure using CloudFormation:

```bash
# Deploy main infrastructure
./infrastructure/deploy.sh prod

# Deploy monitoring stack
aws cloudformation create-stack \
  --stack-name content-aggregator-prod-monitoring \
  --template-body file://infrastructure/monitoring-stack.yml \
  --parameters ParameterKey=Environment,ParameterValue=prod \
               ParameterKey=AlertEmail,ParameterValue=admin@yourcompany.com \
  --capabilities CAPABILITY_IAM
```

### 2. Database Setup

The RDS PostgreSQL instance is created automatically. Configure the database:

```bash
# Get database endpoint
DB_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name content-aggregator-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
  --output text)

# Database will be automatically initialized by the application
echo "Database endpoint: $DB_ENDPOINT"
```

### 3. Application Deployment

The CI/CD pipeline automatically deploys when code is pushed to main:

```bash
# Manual deployment (if needed)
git push origin main

# Or trigger manual deployment
gh workflow run "Full Stack CI/CD Pipeline"
```

### 4. Validation

Validate the deployment:

```bash
# Get ALB DNS name
ALB_DNS=$(aws cloudformation describe-stacks \
  --stack-name content-aggregator-prod \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
  --output text)

# Run validation tests
python3 tests/validate_deployment.py --url "http://$ALB_DNS" --wait
```

## CI/CD Pipeline

### Pipeline Stages

1. **Testing Phase:**
   - Frontend: Linting, unit tests, build verification
   - Backend: Linting, type checking, unit tests with PostgreSQL
   - Security: Trivy vulnerability scanning

2. **Deployment Phase:**
   - Build and push Docker image to ECR
   - Update ECS service with new image
   - Deploy frontend to Vercel
   - Run health checks

3. **Validation Phase:**
   - Application health checks
   - Performance validation
   - Rollback on failure

### Environments

- **Development:** Auto-deploy from `develop` branch
- **Staging:** Manual approval required
- **Production:** Auto-deploy from `main` branch with full validation

## Monitoring & Alerting

### CloudWatch Dashboard

Access the monitoring dashboard:
```
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=prod-content-aggregator-monitoring
```

### Key Metrics Monitored

- **Application Health:** Response time, error rates, availability
- **Infrastructure:** CPU, memory, network utilization
- **Database:** Connection count, query performance, storage
- **Load Balancer:** Request count, response codes, latency

### Alerts Configuration

Alerts are sent via SNS to the configured email address for:
- High CPU/Memory utilization (>80%)
- High error rate (>10 errors/5min)
- Low healthy host count (<1)
- Database connection issues

## Rollback Procedures

### Automatic Rollback

The CI/CD pipeline automatically rolls back on:
- Failed health checks
- Deployment timeout
- Critical errors during deployment

### Manual Rollback

```bash
# List available versions
./scripts/rollback.sh --list

# Rollback to previous version
./scripts/rollback.sh prod

# Rollback to specific version
./scripts/rollback.sh prod 123

# Emergency rollback (skip confirmations)
./scripts/rollback.sh --emergency prod
```

## Security Considerations

### Network Security
- VPC with public/private subnets
- Security groups with minimal required access
- Database in private subnets only
- HTTPS termination at load balancer

### Application Security
- Secrets stored in AWS Secrets Manager
- Container images scanned for vulnerabilities
- IAM roles with least privilege access
- Database encryption at rest

### Monitoring Security
- CloudTrail for API logging
- VPC Flow Logs for network monitoring
- Container insights for runtime security

## Scaling Configuration

### Auto Scaling

ECS Service auto-scaling is configured based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)
- Request count per target

```bash
# Update auto-scaling configuration
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/content-aggregator-prod/content-aggregator-service \
  --min-capacity 2 \
  --max-capacity 10
```

### Database Scaling

RDS instance can be scaled:
- Vertically: Change instance class
- Storage: Auto-scaling enabled
- Read replicas: For read-heavy workloads

## Backup & Recovery

### Database Backups
- Automated daily backups (7-day retention)
- Point-in-time recovery enabled
- Cross-region backup replication (optional)

### Application Data
- Container images stored in ECR with lifecycle policies
- Configuration stored in version control
- Secrets backed up in Secrets Manager

## Cost Optimization

### Current Estimated Costs (Monthly)
- **ECS Fargate:** ~$30-50 (2 tasks, 0.5 vCPU, 1GB RAM)
- **RDS PostgreSQL:** ~$15-25 (db.t3.micro)
- **Application Load Balancer:** ~$20
- **Data Transfer:** ~$5-15
- **CloudWatch:** ~$5-10
- **Total:** ~$75-120/month

### Cost Optimization Tips
1. Use Fargate Spot for non-critical workloads
2. Enable RDS storage auto-scaling
3. Set up CloudWatch billing alerts
4. Review and optimize unused resources monthly

## Troubleshooting

### Common Issues

1. **Deployment Fails:**
   ```bash
   # Check ECS service events
   aws ecs describe-services --cluster content-aggregator-prod --services content-aggregator-service
   
   # Check CloudWatch logs
   aws logs tail /ecs/content-aggregator-prod --follow
   ```

2. **Health Check Failures:**
   ```bash
   # Check target group health
   aws elbv2 describe-target-health --target-group-arn <target-group-arn>
   
   # Test health endpoint directly
   curl -v http://<alb-dns>/health
   ```

3. **Database Connection Issues:**
   ```bash
   # Check security group rules
   aws ec2 describe-security-groups --group-ids <db-security-group-id>
   
   # Test database connectivity from ECS task
   aws ecs run-task --cluster content-aggregator-prod --task-definition content-aggregator-prod --overrides '{"containerOverrides":[{"name":"content-aggregator","command":["python","-c","import psycopg2; print(\"DB OK\")"]}]}'
   ```

### Support Contacts

- **Infrastructure Issues:** DevOps Team
- **Application Issues:** Development Team
- **Security Issues:** Security Team

## Maintenance Windows

- **Scheduled Maintenance:** Sundays 2-4 AM UTC
- **Emergency Maintenance:** As needed with 1-hour notice
- **Database Maintenance:** Automated during maintenance window

---

For additional support or questions, please refer to the project documentation or contact the development team.
