from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.content import Content
from app.models.tag import Tag, content_tags
from app.models.category import Category
from app.models.content_source import ContentSource
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class OverviewStats(BaseModel):
    total_content: int
    total_tags: int
    total_categories: int
    total_sources: int
    content_this_week: int
    content_this_month: int

class ContentTypeStats(BaseModel):
    content_type: str
    count: int

class TagStats(BaseModel):
    id: int
    name: str
    count: int

class CategoryStats(BaseModel):
    id: int
    name: str
    count: int

class TimeSeriesPoint(BaseModel):
    date: str
    count: int

class AnalyticsResponse(BaseModel):
    overview: OverviewStats
    content_by_type: List[ContentTypeStats]
    top_tags: List[TagStats]
    top_categories: List[CategoryStats]
    content_over_time: List[TimeSeriesPoint]

@router.get("/overview", response_model=AnalyticsResponse)
def get_analytics_overview(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive analytics overview"""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    start_date = now - timedelta(days=days)

    # Overview stats
    total_content = db.query(Content).filter(Content.user_id == current_user.id).count()
    total_tags = db.query(Tag).count()
    total_categories = db.query(Category).filter(Category.user_id == current_user.id).count()
    total_sources = db.query(ContentSource).filter(ContentSource.user_id == current_user.id).count()

    content_this_week = db.query(Content).filter(
        Content.user_id == current_user.id,
        Content.created_at >= week_ago
    ).count()

    content_this_month = db.query(Content).filter(
        Content.user_id == current_user.id,
        Content.created_at >= month_ago
    ).count()

    overview = OverviewStats(
        total_content=total_content,
        total_tags=total_tags,
        total_categories=total_categories,
        total_sources=total_sources,
        content_this_week=content_this_week,
        content_this_month=content_this_month
    )

    # Content by type
    type_stats = db.query(
        Content.content_type,
        func.count(Content.id).label('count')
    ).filter(
        Content.user_id == current_user.id
    ).group_by(Content.content_type).all()

    content_by_type = [
        ContentTypeStats(content_type=t[0], count=t[1]) for t in type_stats
    ]

    # Top tags (by usage count)
    tag_stats = db.query(
        Tag.id,
        Tag.name,
        func.count(content_tags.c.content_id).label('count')
    ).join(
        content_tags, Tag.id == content_tags.c.tag_id
    ).join(
        Content, Content.id == content_tags.c.content_id
    ).filter(
        Content.user_id == current_user.id
    ).group_by(Tag.id, Tag.name).order_by(desc('count')).limit(10).all()

    top_tags = [
        TagStats(id=t[0], name=t[1], count=t[2]) for t in tag_stats
    ]

    # Top categories (by content count)
    cat_stats = db.query(
        Category.id,
        Category.name,
        func.count(Content.id).label('count')
    ).outerjoin(
        Content, Content.category_id == Category.id
    ).filter(
        Category.user_id == current_user.id
    ).group_by(Category.id, Category.name).order_by(desc('count')).limit(10).all()

    top_categories = [
        CategoryStats(id=c[0], name=c[1], count=c[2]) for c in cat_stats
    ]

    # Content over time (daily counts for the period)
    content_over_time = []
    for i in range(days):
        day = start_date + timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        count = db.query(Content).filter(
            Content.user_id == current_user.id,
            Content.created_at >= day_start,
            Content.created_at < day_end
        ).count()

        content_over_time.append(
            TimeSeriesPoint(date=day_start.strftime('%Y-%m-%d'), count=count)
        )

    return AnalyticsResponse(
        overview=overview,
        content_by_type=content_by_type,
        top_tags=top_tags,
        top_categories=top_categories,
        content_over_time=content_over_time
    )

@router.get("/export")
def export_analytics(
    format: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export analytics data as JSON or CSV"""
    from fastapi.responses import Response

    analytics = get_analytics_overview(days=days, db=db, current_user=current_user)

    if format == "json":
        import json
        content = json.dumps(analytics.model_dump(), indent=2)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=analytics.json"}
        )
    else:
        # CSV format
        lines = ["metric,value"]
        lines.append(f"total_content,{analytics.overview.total_content}")
        lines.append(f"total_tags,{analytics.overview.total_tags}")
        lines.append(f"total_categories,{analytics.overview.total_categories}")
        lines.append(f"total_sources,{analytics.overview.total_sources}")
        lines.append(f"content_this_week,{analytics.overview.content_this_week}")
        lines.append(f"content_this_month,{analytics.overview.content_this_month}")
        lines.append("")
        lines.append("content_type,count")
        for item in analytics.content_by_type:
            lines.append(f"{item.content_type},{item.count}")
        lines.append("")
        lines.append("tag,count")
        for item in analytics.top_tags:
            lines.append(f"{item.name},{item.count}")

        content = "\n".join(lines)
        return Response(
            content=content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=analytics.csv"}
        )
