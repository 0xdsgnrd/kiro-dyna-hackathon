from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import secrets
from datetime import datetime, timezone
from app.db.session import get_db
from app.models.user import User
from app.models.content import Content
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ShareRequest(BaseModel):
    is_public: bool

class ShareResponse(BaseModel):
    id: int
    title: str
    is_public: bool
    share_token: Optional[str]
    share_url: Optional[str]

class PublicContentResponse(BaseModel):
    id: int
    title: str
    url: Optional[str]
    content_text: Optional[str]
    content_type: str
    created_at: datetime
    owner_username: str

    class Config:
        from_attributes = True

@router.put("/{content_id}/share", response_model=ShareResponse)
def toggle_content_sharing(
    content_id: int,
    share_request: ShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle public sharing for a content item"""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    content.is_public = share_request.is_public

    if share_request.is_public and not content.share_token:
        content.share_token = secrets.token_urlsafe(16)

    db.commit()
    db.refresh(content)

    share_url = f"/shared/{content.share_token}" if content.is_public else None

    return ShareResponse(
        id=content.id,
        title=content.title,
        is_public=content.is_public,
        share_token=content.share_token if content.is_public else None,
        share_url=share_url
    )

@router.get("/my-shared", response_model=List[ShareResponse])
def list_my_shared_content(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all content shared by current user"""
    contents = db.query(Content).filter(
        Content.user_id == current_user.id,
        Content.is_public == True
    ).all()

    return [
        ShareResponse(
            id=c.id,
            title=c.title,
            is_public=c.is_public,
            share_token=c.share_token,
            share_url=f"/shared/{c.share_token}"
        ) for c in contents
    ]

# Public endpoint - no authentication required
@router.get("/public/{share_token}", response_model=PublicContentResponse)
def get_public_content(
    share_token: str,
    db: Session = Depends(get_db)
):
    """Get publicly shared content by share token (no auth required)"""
    content = db.query(Content).filter(
        Content.share_token == share_token,
        Content.is_public == True
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Shared content not found")

    # Increment view count
    if hasattr(content, 'view_count'):
        content.view_count = (content.view_count or 0) + 1
        db.commit()

    return PublicContentResponse(
        id=content.id,
        title=content.title,
        url=content.url,
        content_text=content.content_text,
        content_type=content.content_type,
        created_at=content.created_at,
        owner_username=content.user.username
    )

@router.get("/discover", response_model=List[PublicContentResponse])
def discover_public_content(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Discover recently shared public content (no auth required)"""
    contents = db.query(Content).filter(
        Content.is_public == True
    ).order_by(Content.created_at.desc()).offset(skip).limit(limit).all()

    return [
        PublicContentResponse(
            id=c.id,
            title=c.title,
            url=c.url,
            content_text=c.content_text,
            content_type=c.content_type,
            created_at=c.created_at,
            owner_username=c.user.username
        ) for c in contents
    ]
