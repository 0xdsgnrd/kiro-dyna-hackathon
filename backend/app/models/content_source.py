from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ContentSource(Base):
    __tablename__ = "content_sources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    source_type = Column(String(50), nullable=False)  # rss, webpage
    active = Column(Boolean, default=True)
    last_fetched = Column(DateTime(timezone=True), nullable=True)
    error_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships with string references to avoid circular imports
    user = relationship("User", back_populates="content_sources")
    contents = relationship("Content", back_populates="source")
    import_logs = relationship("ImportLog", back_populates="source", cascade="all, delete-orphan")

class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("content_sources.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)  # success, error, partial
    items_imported = Column(Integer, default=0)
    items_skipped = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships with string references to avoid circular imports
    source = relationship("ContentSource", back_populates="import_logs")
