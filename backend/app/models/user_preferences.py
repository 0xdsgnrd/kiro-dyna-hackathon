from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Theme settings
    theme = Column(String(20), default="system")  # light, dark, system

    # Default content settings
    default_content_type = Column(String(50), default="article")

    # Dashboard settings
    dashboard_layout = Column(JSON, default=lambda: {
        "show_recent_content": True,
        "show_stats": True,
        "show_sources": True,
        "show_tags": True
    })

    # Notification settings
    email_notifications = Column(Boolean, default=True)

    # Other preferences
    items_per_page = Column(Integer, default=20)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")
