import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.routes import auth, content, tags, categories, content_sources
from app.services.background_import import background_service

# Import all models to ensure they're registered
from app.models import user, content, tag, category, content_source

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background import service
    task = asyncio.create_task(background_service.start_scheduler())
    yield
    # Stop background service
    background_service.stop_scheduler()
    task.cancel()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(content_sources.router, prefix="/api/v1/sources", tags=["content-sources"])

@app.get("/")
def root():
    return {"message": "Content Aggregation API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
