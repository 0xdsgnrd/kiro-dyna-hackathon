from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.tag import content_tags

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey("content_sources.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=True)
    content_text = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=False)  # article, video, note, link
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Sharing fields
    is_public = Column(Boolean, default=False)
    share_token = Column(String(32), unique=True, nullable=True, index=True)
    view_count = Column(Integer, default=0)

    # Intelligence fields
    reading_time = Column(Integer, nullable=True)  # minutes
    quality_score = Column(Integer, nullable=True)  # 0-100

    # Relationships with string references to avoid circular imports
    user = relationship("User", back_populates="contents")
    source = relationship("ContentSource", back_populates="contents")
    category = relationship("Category", back_populates="contents")
    tags = relationship("Tag", secondary=content_tags, back_populates="contents")
