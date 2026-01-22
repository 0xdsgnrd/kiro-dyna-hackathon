"""
Application metrics and monitoring utilities
"""
import time
import logging
from typing import Dict, Any
from functools import wraps
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        if settings.ENVIRONMENT == "production":
            self.cloudwatch = boto3.client('cloudwatch', region_name=settings.AWS_REGION)
        else:
            self.cloudwatch = None
    
    def put_metric(self, metric_name: str, value: float, unit: str = 'Count', dimensions: Dict[str, str] = None):
        """Send custom metric to CloudWatch"""
        if not self.cloudwatch:
            logger.info(f"Metric (dev): {metric_name}={value} {unit}")
            return
        
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': time.time()
            }
            
            if dimensions:
                metric_data['Dimensions'] = [
                    {'Name': k, 'Value': v} for k, v in dimensions.items()
                ]
            
            self.cloudwatch.put_metric_data(
                Namespace=f'{settings.PROJECT_NAME}/Application',
                MetricData=[metric_data]
            )
        except ClientError as e:
            logger.error(f"Failed to send metric {metric_name}: {e}")
    
    def increment_counter(self, metric_name: str, dimensions: Dict[str, str] = None):
        """Increment a counter metric"""
        self.put_metric(metric_name, 1, 'Count', dimensions)
    
    def record_latency(self, metric_name: str, latency_ms: float, dimensions: Dict[str, str] = None):
        """Record latency metric"""
        self.put_metric(metric_name, latency_ms, 'Milliseconds', dimensions)
    
    def record_health_check_failure(self):
        """Record health check failure"""
        self.put_metric('HealthCheckFailed', 1, 'Count')

# Global metrics collector instance
metrics = MetricsCollector()

def monitor_performance(metric_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                latency = (time.time() - start_time) * 1000
                name = metric_name or f"{func.__name__}_latency"
                metrics.record_latency(name, latency)
                return result
            except Exception as e:
                metrics.increment_counter(f"{func.__name__}_error")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                latency = (time.time() - start_time) * 1000
                name = metric_name or f"{func.__name__}_latency"
                metrics.record_latency(name, latency)
                return result
            except Exception as e:
                metrics.increment_counter(f"{func.__name__}_error")
                raise
        
        return async_wrapper if hasattr(func, '__code__') and func.__code__.co_flags & 0x80 else sync_wrapper
    return decorator

class HealthMetrics:
    """Health check metrics collection"""
    
    @staticmethod
    def record_api_request(endpoint: str, method: str, status_code: int, response_time: float):
        """Record API request metrics"""
        dimensions = {
            'Endpoint': endpoint,
            'Method': method,
            'StatusCode': str(status_code)
        }
        
        metrics.increment_counter('APIRequest', dimensions)
        metrics.record_latency('APILatency', response_time * 1000, dimensions)
        
        if status_code >= 400:
            metrics.increment_counter('APIError', dimensions)
    
    @staticmethod
    def record_database_operation(operation: str, success: bool, duration: float):
        """Record database operation metrics"""
        dimensions = {
            'Operation': operation,
            'Status': 'Success' if success else 'Error'
        }
        
        metrics.increment_counter('DatabaseOperation', dimensions)
        metrics.record_latency('DatabaseLatency', duration * 1000, dimensions)
    
    @staticmethod
    def record_user_activity(activity: str, user_id: str = None):
        """Record user activity metrics"""
        dimensions = {'Activity': activity}
        if user_id:
            dimensions['UserType'] = 'Authenticated'
        else:
            dimensions['UserType'] = 'Anonymous'
        
        metrics.increment_counter('UserActivity', dimensions)
