from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.content_source import ContentSource, ImportLog
from app.schemas.content_source import (
    ContentSourceCreate, 
    ContentSourceUpdate, 
    ContentSourceResponse,
    ImportLogResponse,
    ImportStatusResponse
)
from app.api.deps import get_current_user
from app.services.content_import import ContentImportService

router = APIRouter()

@router.post("", response_model=ContentSourceResponse, status_code=status.HTTP_201_CREATED)
def create_content_source(
    source_data: ContentSourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new content source"""
    source = ContentSource(
        user_id=current_user.id,
        name=source_data.name,
        url=source_data.url,
        source_type=source_data.source_type
    )
    
    db.add(source)
    db.commit()
    db.refresh(source)
    return source

@router.get("", response_model=List[ContentSourceResponse])
def list_content_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all content sources for the current user"""
    sources = db.query(ContentSource).filter(
        ContentSource.user_id == current_user.id
    ).order_by(ContentSource.created_at.desc()).all()
    return sources

@router.get("/{source_id}", response_model=ContentSourceResponse)
def get_content_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific content source"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    return source

@router.put("/{source_id}", response_model=ContentSourceResponse)
def update_content_source(
    source_id: int,
    source_data: ContentSourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a content source"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    if source_data.name is not None:
        source.name = source_data.name
    if source_data.url is not None:
        source.url = source_data.url
    if source_data.active is not None:
        source.active = source_data.active
    
    db.commit()
    db.refresh(source)
    return source

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a content source"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    db.delete(source)
    db.commit()
    return None

@router.post("/{source_id}/import", response_model=ImportStatusResponse)
async def import_from_source(
    source_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually trigger import from a content source"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    if not source.active:
        raise HTTPException(status_code=400, detail="Content source is inactive")
    
    # Run import in background
    import_service = ContentImportService(db)
    result = await import_service.import_from_source(source_id)
    
    return ImportStatusResponse(
        source_id=source_id,
        status=result["status"],
        message=result.get("message", "Import completed"),
        items_imported=result.get("items_imported", 0),
        items_skipped=result.get("items_skipped", 0)
    )

@router.get("/{source_id}/logs", response_model=List[ImportLogResponse])
def get_import_logs(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get import logs for a content source"""
    source = db.query(ContentSource).filter(
        ContentSource.id == source_id,
        ContentSource.user_id == current_user.id
    ).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Content source not found")
    
    logs = db.query(ImportLog).filter(
        ImportLog.source_id == source_id
    ).order_by(ImportLog.started_at.desc()).limit(20).all()
    
    return logs
