from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.content import Content
from app.models.tag import Tag
from app.models.category import Category
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
def create_content(
    content_data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate category belongs to user if provided
    if content_data.category_id:
        category = db.query(Category).filter(
            Category.id == content_data.category_id,
            Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Create content
    content = Content(
        user_id=current_user.id,
        title=content_data.title,
        url=content_data.url,
        content_text=content_data.content_text,
        content_type=content_data.content_type,
        category_id=content_data.category_id
    )
    
    # Add tags
    if content_data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(content_data.tag_ids)).all()
        content.tags = tags
    
    db.add(content)
    db.commit()
    db.refresh(content)
    return content

@router.get("", response_model=List[ContentResponse])
def list_content(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = db.query(Content).filter(
        Content.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return contents

@router.get("/search", response_model=List[ContentResponse])
def search_content(
    q: str = Query("", description="Search query for title, content, or tags"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    tag_id: Optional[int] = Query(None, description="Filter by tag ID"),
    sort_by: str = Query("created_at", description="Sort field: created_at or title"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Content).filter(Content.user_id == current_user.id)
    
    # Search filter
    if q:
        query = query.filter(
            (Content.title.ilike(f"%{q}%")) | 
            (Content.content_text.ilike(f"%{q}%"))
        )
    
    # Category filter
    if category_id is not None:
        query = query.filter(Content.category_id == category_id)
    
    # Content type filter
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    # Tag filter
    if tag_id is not None:
        query = query.join(Content.tags).filter(Tag.id == tag_id)
    
    # Sorting
    if sort_by == "title":
        query = query.order_by(Content.title.desc() if sort_order == "desc" else Content.title.asc())
    else:
        query = query.order_by(Content.created_at.desc() if sort_order == "desc" else Content.created_at.asc())
    
    contents = query.offset(skip).limit(limit).all()
    return contents

@router.get("/{content_id}", response_model=ContentResponse)
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content

@router.put("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    content_data: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Update fields
    if content_data.title is not None:
        content.title = content_data.title
    if content_data.url is not None:
        content.url = content_data.url
    if content_data.content_text is not None:
        content.content_text = content_data.content_text
    if content_data.content_type is not None:
        content.content_type = content_data.content_type
    if content_data.category_id is not None:
        # Validate category
        category = db.query(Category).filter(
            Category.id == content_data.category_id,
            Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        content.category_id = content_data.category_id
    
    # Update tags
    if content_data.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(content_data.tag_ids)).all()
        content.tags = tags
    
    db.commit()
    db.refresh(content)
    return content

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(content)
    db.commit()
    return None
