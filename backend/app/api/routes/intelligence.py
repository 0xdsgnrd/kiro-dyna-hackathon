from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.content import Content
from app.api.deps import get_current_user
from app.services.content_intelligence import ContentIntelligenceService
from pydantic import BaseModel

router = APIRouter()

class TagSuggestion(BaseModel):
    tag: str
    confidence: float
    is_existing: bool

class ContentAnalysis(BaseModel):
    content_id: int
    suggested_tags: List[TagSuggestion]
    reading_time: int
    quality_score: int
    word_count: int

class RelatedContent(BaseModel):
    id: int
    title: str
    content_type: str
    similarity: float

class BatchAnalysisResult(BaseModel):
    analyzed: int
    suggestions: List[dict]

@router.get("/analyze/{content_id}", response_model=ContentAnalysis)
def analyze_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze a content item for tags, reading time, and quality"""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()

    if not content:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Content not found")

    service = ContentIntelligenceService(db)
    analysis = service.analyze_content(content)

    return ContentAnalysis(
        content_id=content.id,
        suggested_tags=[TagSuggestion(**t) for t in analysis["suggested_tags"]],
        reading_time=analysis["reading_time"],
        quality_score=analysis["quality_score"],
        word_count=analysis["word_count"]
    )

@router.get("/related/{content_id}", response_model=List[RelatedContent])
def get_related_content(
    content_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get related content based on tags and similarity"""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()

    if not content:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Content not found")

    service = ContentIntelligenceService(db)
    related = service.find_related_content(content, limit)

    return [
        RelatedContent(
            id=item.id,
            title=item.title,
            content_type=item.content_type,
            similarity=similarity
        ) for item, similarity in related
    ]

@router.post("/suggest-tags")
def suggest_tags_for_text(
    text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tag suggestions for arbitrary text"""
    service = ContentIntelligenceService(db)
    suggestions = service.suggest_tags(text)

    return {"suggestions": suggestions}

@router.post("/batch-analyze", response_model=BatchAnalysisResult)
def batch_analyze_content(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze all user's content and update intelligence metadata"""
    service = ContentIntelligenceService(db)
    result = service.batch_analyze(current_user.id, limit)

    return BatchAnalysisResult(**result)
