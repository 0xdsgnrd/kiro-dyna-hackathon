"""
Database health check and monitoring utilities
"""
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseHealthCheck:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
    
    def check_connection(self) -> bool:
        """Test basic database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def check_tables(self) -> dict:
        """Check if all required tables exist"""
        required_tables = [
            'users', 'contents', 'tags', 'categories', 
            'content_sources', 'content_tags', 'user_preferences'
        ]
        
        results = {}
        try:
            with self.engine.connect() as conn:
                for table in required_tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.scalar()
                        results[table] = {'exists': True, 'count': count}
                    except Exception as e:
                        results[table] = {'exists': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Failed to check tables: {e}")
            return {'error': str(e)}
        
        return results
    
    def check_performance(self) -> dict:
        """Basic performance check"""
        try:
            start_time = time.time()
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            response_time = (time.time() - start_time) * 1000  # ms
            
            return {
                'response_time_ms': round(response_time, 2),
                'status': 'healthy' if response_time < 100 else 'slow'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'unhealthy'}
    
    def full_health_check(self) -> dict:
        """Comprehensive health check"""
        return {
            'connection': self.check_connection(),
            'tables': self.check_tables(),
            'performance': self.check_performance(),
            'timestamp': time.time()
        }

# Health check endpoint function
def get_database_health():
    """Function to be used by FastAPI health endpoint"""
    health_checker = DatabaseHealthCheck()
    return health_checker.full_health_check()
