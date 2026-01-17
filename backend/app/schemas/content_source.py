from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List

# Content Source Schemas
class ContentSourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    url: str = Field(..., min_length=1, max_length=500)
    source_type: str = Field(..., pattern="^(rss|webpage)$")

class ContentSourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[str] = Field(None, min_length=1, max_length=500)
    active: Optional[bool] = None

class ContentSourceResponse(BaseModel):
    id: int
    user_id: int
    name: str
    url: str
    source_type: str
    active: bool
    last_fetched: Optional[datetime]
    error_count: int
    last_error: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Import Log Schemas
class ImportLogResponse(BaseModel):
    id: int
    source_id: int
    status: str
    items_imported: int
    items_skipped: int
    error_message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Import Status Schema
class ImportStatusResponse(BaseModel):
    source_id: int
    status: str
    message: str
    items_imported: int = 0
    items_skipped: int = 0
