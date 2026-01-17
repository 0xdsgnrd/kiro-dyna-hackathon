from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DashboardLayout(BaseModel):
    show_recent_content: bool = True
    show_stats: bool = True
    show_sources: bool = True
    show_tags: bool = True

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = Field(None, pattern="^(light|dark|system)$")
    default_content_type: Optional[str] = Field(None, pattern="^(article|video|note|link)$")
    dashboard_layout: Optional[DashboardLayout] = None
    email_notifications: Optional[bool] = None
    items_per_page: Optional[int] = Field(None, ge=10, le=100)

class UserPreferencesResponse(BaseModel):
    id: int
    user_id: int
    theme: str
    default_content_type: str
    dashboard_layout: Dict[str, Any]
    email_notifications: bool
    items_per_page: int

    class Config:
        from_attributes = True
