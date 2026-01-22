# Monitoring and Observability Guide

## Overview

Comprehensive monitoring and observability setup for the Content Aggregation Platform, including CloudWatch metrics, alarms, dashboards, and uptime monitoring.

## Architecture

```
Application → Metrics → CloudWatch → Alarms → SNS → Email/SMS
           → Logs → CloudWatch Logs → Dashboard
           → Health Checks → Uptime Monitor → Alerts
```

## Components

### 1. CloudWatch Infrastructure

**Monitoring Stack**: `infrastructure/monitoring-stack.yml`
- SNS topics for alerts
- CloudWatch log groups
- Performance alarms (CPU, Memory, Database)
- Health check failure alarms
- Comprehensive dashboard

### 2. Application Metrics

**Metrics Collection**: `backend/app/monitoring/metrics.py`
- Custom CloudWatch metrics
- Performance monitoring decorators
- Health check metrics
- User activity tracking

**Request Monitoring**: `backend/app/monitoring/middleware.py`
- API request/response metrics
- Response time tracking
- Error rate monitoring
- Request logging

### 3. Uptime Monitoring

**External Monitoring**: `infrastructure/setup-uptime-monitoring.sh`
- Independent health checks
- Failure detection and alerting
- Service recovery notifications
- Detailed health monitoring

## Setup Instructions

### 1. Deploy Monitoring Infrastructure

```bash
# Deploy monitoring stack
aws cloudformation create-stack \
    --stack-name content-aggregator-monitoring \
    --template-body file://infrastructure/monitoring-stack.yml \
    --parameters ParameterKey=ProjectName,ParameterValue=content-aggregator \
                 ParameterKey=Environment,ParameterValue=prod \
                 ParameterKey=AlertEmail,ParameterValue=your-email@example.com
```

### 2. Configure Application Metrics

Application metrics are automatically enabled in production. Required environment variables:

```bash
ENVIRONMENT=production
AWS_REGION=us-east-1
PROJECT_NAME=Content Aggregation API
```

### 3. Set Up Uptime Monitoring

```bash
# Generate monitoring setup
cd infrastructure
./setup-uptime-monitoring.sh

# Deploy to monitoring server
python3 uptime_monitor.py https://your-api.com [SNS_TOPIC_ARN]
```

## Monitoring Features

### CloudWatch Metrics

**System Metrics:**
- ECS CPU and Memory utilization
- RDS performance and connections
- Application response times
- Error rates and counts

**Custom Metrics:**
- API request counts by endpoint
- Database operation latencies
- User activity patterns
- Health check failures

### Alarms and Alerts

**Critical Alarms:**
- High CPU utilization (>80%)
- High memory usage (>85%)
- Database connection exhaustion (>15)
- Health check failures (≥3)

**Alert Channels:**
- Email notifications via SNS
- CloudWatch dashboard updates
- Application logs

### Dashboard Views

**Performance Dashboard:**
- Real-time resource utilization
- API response times
- Database performance metrics
- Recent error logs

**Health Dashboard:**
- Service status overview
- Database connectivity
- Response time trends
- Error rate analysis

## Metrics Reference

### Application Metrics

| Metric Name | Type | Description |
|-------------|------|-------------|
| `APIRequest` | Counter | API requests by endpoint/method/status |
| `APILatency` | Timer | API response times |
| `APIError` | Counter | API error counts |
| `DatabaseOperation` | Counter | Database operations by type |
| `DatabaseLatency` | Timer | Database query response times |
| `UserActivity` | Counter | User actions and engagement |
| `HealthCheckFailed` | Counter | Health check failures |

### AWS Metrics

| Metric Name | Namespace | Description |
|-------------|-----------|-------------|
| `CPUUtilization` | AWS/ECS | Container CPU usage |
| `MemoryUtilization` | AWS/ECS | Container memory usage |
| `DatabaseConnections` | AWS/RDS | Active database connections |
| `ReadLatency` | AWS/RDS | Database read latency |
| `WriteLatency` | AWS/RDS | Database write latency |

## Alerting Rules

### Critical Alerts (Immediate Response)
- Service completely down (health check failures)
- Database connection failures
- High error rates (>5% of requests)

### Warning Alerts (Monitor Closely)
- High resource utilization (CPU >80%, Memory >85%)
- Slow response times (>2 seconds)
- Elevated error rates (>1% of requests)

### Info Alerts (Awareness)
- Unusual traffic patterns
- Performance degradation trends
- Resource usage trends

## Troubleshooting

### High CPU/Memory Usage
```bash
# Check ECS service metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=content-aggregator-service \
  --start-time 2026-01-20T12:00:00Z \
  --end-time 2026-01-20T13:00:00Z \
  --period 300 \
  --statistics Average
```

### Database Performance Issues
```bash
# Check RDS performance
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=content-aggregator-prod-db \
  --start-time 2026-01-20T12:00:00Z \
  --end-time 2026-01-20T13:00:00Z \
  --period 300 \
  --statistics Average
```

### Application Errors
```bash
# Check application logs
aws logs filter-log-events \
  --log-group-name /ecs/content-aggregator-prod \
  --filter-pattern "ERROR" \
  --start-time 1642680000000
```

## Performance Optimization

### Metric Collection Optimization
- Batch metric submissions to reduce API calls
- Use appropriate metric units and dimensions
- Implement metric sampling for high-volume events

### Alert Optimization
- Set appropriate thresholds to avoid alert fatigue
- Use composite alarms for complex conditions
- Implement escalation policies

### Dashboard Optimization
- Focus on key performance indicators
- Use appropriate time ranges and aggregations
- Organize metrics by service and priority

## Cost Management

### CloudWatch Costs
- Monitor custom metric usage
- Optimize log retention periods
- Use metric filters to reduce log ingestion
- Archive old metrics and logs

### Estimated Monthly Costs (Production)
- Custom Metrics: ~$15/month (500 metrics)
- Log Ingestion: ~$10/month (10GB)
- Dashboard: ~$3/month (1 dashboard)
- Alarms: ~$1/month (10 alarms)
- **Total**: ~$29/month

## Security Considerations

- IAM roles with minimal required permissions
- Encrypted log storage
- Secure SNS topic access
- VPC endpoints for CloudWatch (optional)
- No sensitive data in metrics or logs

## Maintenance

### Regular Tasks
- Review and update alarm thresholds
- Clean up old log groups
- Monitor CloudWatch costs
- Update dashboard widgets
- Test alert notifications

### Quarterly Reviews
- Analyze performance trends
- Optimize metric collection
- Review alert effectiveness
- Update monitoring documentation
