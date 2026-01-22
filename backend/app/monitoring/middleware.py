"""
Request monitoring middleware for FastAPI
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.monitoring.metrics import HealthMetrics

logger = logging.getLogger(__name__)

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to monitor API requests and performance"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Extract request info
        method = request.method
        path = request.url.path
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate response time
            process_time = time.time() - start_time
            
            # Record metrics
            HealthMetrics.record_api_request(
                endpoint=path,
                method=method,
                status_code=response.status_code,
                response_time=process_time
            )
            
            # Add response headers
            response.headers["X-Process-Time"] = str(process_time)
            
            # Log request
            logger.info(
                f"{method} {path} - {response.status_code} - {process_time:.3f}s"
            )
            
            return response
            
        except Exception as e:
            # Record error metrics
            process_time = time.time() - start_time
            HealthMetrics.record_api_request(
                endpoint=path,
                method=method,
                status_code=500,
                response_time=process_time
            )
            
            logger.error(f"{method} {path} - ERROR: {str(e)} - {process_time:.3f}s")
            raise
