from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Tag Schemas
class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class TagResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Category Schemas
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Content Schemas
class ContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    url: Optional[str] = Field(None, max_length=500)
    content_text: Optional[str] = None
    content_type: str = Field(..., pattern="^(article|video|note|link)$")
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[str] = Field(None, max_length=500)
    content_text: Optional[str] = None
    content_type: Optional[str] = Field(None, pattern="^(article|video|note|link)$")
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class ContentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    url: Optional[str]
    content_text: Optional[str]
    content_type: str
    category_id: Optional[int]
    category: Optional[CategoryResponse]
    tags: List[TagResponse]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
