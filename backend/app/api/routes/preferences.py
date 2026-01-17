from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.schemas.user_preferences import UserPreferencesUpdate, UserPreferencesResponse
from app.api.deps import get_current_user

router = APIRouter()

def get_or_create_preferences(db: Session, user_id: int) -> UserPreferences:
    """Get user preferences or create with defaults"""
    prefs = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    if not prefs:
        prefs = UserPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    return prefs

@router.get("", response_model=UserPreferencesResponse)
def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's preferences"""
    return get_or_create_preferences(db, current_user.id)

@router.put("", response_model=UserPreferencesResponse)
def update_preferences(
    prefs_data: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's preferences"""
    prefs = get_or_create_preferences(db, current_user.id)

    if prefs_data.theme is not None:
        prefs.theme = prefs_data.theme
    if prefs_data.default_content_type is not None:
        prefs.default_content_type = prefs_data.default_content_type
    if prefs_data.dashboard_layout is not None:
        prefs.dashboard_layout = prefs_data.dashboard_layout.model_dump()
    if prefs_data.email_notifications is not None:
        prefs.email_notifications = prefs_data.email_notifications
    if prefs_data.items_per_page is not None:
        prefs.items_per_page = prefs_data.items_per_page

    db.commit()
    db.refresh(prefs)
    return prefs
