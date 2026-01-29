import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.db.session import engine, Base
from app.api.routes import auth, content as content_routes, tags, categories, content_sources
from app.api.routes import analytics, preferences, sharing, export_import, intelligence
from app.websocket.routes import router as websocket_router
from app.websocket.manager import heartbeat_task
from app.services.background_import import background_service
from app.monitoring.middleware import MonitoringMiddleware

# Import all models to ensure they're registered
from app.models import user, content as content_model, tag, category, content_source, user_preferences

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background services
    import_task = asyncio.create_task(background_service.start_scheduler())
    heartbeat_task_instance = asyncio.create_task(heartbeat_task())
    
    yield
    
    # Stop background services
    background_service.stop_scheduler()
    import_task.cancel()
    heartbeat_task_instance.cancel()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add monitoring middleware
app.add_middleware(MonitoringMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(content_routes.router, prefix="/api/v1/content", tags=["content"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(content_sources.router, prefix="/api/v1/sources", tags=["content-sources"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(preferences.router, prefix="/api/v1/preferences", tags=["preferences"])
app.include_router(sharing.router, prefix="/api/v1/sharing", tags=["sharing"])
app.include_router(export_import.router, prefix="/api/v1/data", tags=["export-import"])
app.include_router(intelligence.router, prefix="/api/v1/intelligence", tags=["intelligence"])
app.include_router(websocket_router, prefix="/api/v1", tags=["websocket"])

@app.get("/")
def root():
    return {"message": "Content Aggregation API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/health/detailed")
def detailed_health():
    """Detailed health check including database status"""
    from app.db.health import get_database_health
    
    try:
        db_health = get_database_health()
        return {
            "status": "healthy" if db_health.get('connection') else "unhealthy",
            "database": db_health,
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        from app.monitoring.metrics import metrics
        metrics.record_health_check_failure()
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT
        }
