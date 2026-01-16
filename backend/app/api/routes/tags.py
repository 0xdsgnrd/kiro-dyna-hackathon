from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.tag import Tag
from app.schemas.content import TagCreate, TagResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag_data.name.lower()).first()
    if existing_tag:
        return existing_tag
    
    # Create new tag
    tag = Tag(name=tag_data.name.lower())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@router.get("", response_model=List[TagResponse])
def list_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tags = db.query(Tag).all()
    return tags

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return None
