from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import csv
import io
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.models.content import Content
from app.models.tag import Tag, content_tags
from app.models.category import Category
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ExportStats(BaseModel):
    total_content: int
    total_tags: int
    total_categories: int
    format: str
    exported_at: str

class ImportPreview(BaseModel):
    total_items: int
    new_items: int
    duplicate_items: int
    sample_titles: List[str]

class ImportResult(BaseModel):
    success: bool
    items_imported: int
    items_skipped: int
    errors: List[str]

@router.get("/export")
def export_content(
    format: str = Query("json", regex="^(json|csv|opml)$"),
    tag_ids: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export user's content in various formats"""
    query = db.query(Content).filter(Content.user_id == current_user.id)

    if category_id:
        query = query.filter(Content.category_id == category_id)

    if tag_ids:
        tag_id_list = [int(t) for t in tag_ids.split(",")]
        query = query.join(content_tags).filter(content_tags.c.tag_id.in_(tag_id_list))

    contents = query.all()

    if format == "json":
        data = {
            "exported_at": datetime.utcnow().isoformat(),
            "total_items": len(contents),
            "content": [
                {
                    "title": c.title,
                    "url": c.url,
                    "content_text": c.content_text,
                    "content_type": c.content_type,
                    "tags": [t.name for t in c.tags],
                    "category": c.category.name if c.category else None,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                } for c in contents
            ]
        }
        return Response(
            content=json.dumps(data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=content_export.json"}
        )

    elif format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["title", "url", "content_text", "content_type", "tags", "category", "created_at"])

        for c in contents:
            writer.writerow([
                c.title,
                c.url or "",
                c.content_text or "",
                c.content_type,
                ",".join([t.name for t in c.tags]),
                c.category.name if c.category else "",
                c.created_at.isoformat() if c.created_at else ""
            ])

        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=content_export.csv"}
        )

    else:  # OPML
        opml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        opml_content += '<opml version="2.0">\n'
        opml_content += '  <head>\n'
        opml_content += f'    <title>Content Export - {datetime.utcnow().strftime("%Y-%m-%d")}</title>\n'
        opml_content += '  </head>\n'
        opml_content += '  <body>\n'

        for c in contents:
            url = c.url or ""
            opml_content += f'    <outline text="{c.title}" type="link" url="{url}"/>\n'

        opml_content += '  </body>\n'
        opml_content += '</opml>'

        return Response(
            content=opml_content,
            media_type="application/xml",
            headers={"Content-Disposition": "attachment; filename=content_export.opml"}
        )

@router.post("/import/preview", response_model=ImportPreview)
async def preview_import(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Preview import without actually importing"""
    content = await file.read()
    items = _parse_import_file(file.filename, content)

    existing_urls = set(
        url for (url,) in db.query(Content.url).filter(
            Content.user_id == current_user.id,
            Content.url.isnot(None)
        ).all()
    )

    new_items = [i for i in items if i.get("url") not in existing_urls]
    duplicates = len(items) - len(new_items)

    return ImportPreview(
        total_items=len(items),
        new_items=len(new_items),
        duplicate_items=duplicates,
        sample_titles=[i.get("title", "Untitled")[:50] for i in items[:5]]
    )

@router.post("/import", response_model=ImportResult)
async def import_content(
    file: UploadFile = File(...),
    skip_duplicates: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Import content from file"""
    content = await file.read()
    items = _parse_import_file(file.filename, content)

    existing_urls = set()
    if skip_duplicates:
        existing_urls = set(
            url for (url,) in db.query(Content.url).filter(
                Content.user_id == current_user.id,
                Content.url.isnot(None)
            ).all()
        )

    imported = 0
    skipped = 0
    errors = []

    for item in items:
        try:
            if skip_duplicates and item.get("url") in existing_urls:
                skipped += 1
                continue

            content_item = Content(
                user_id=current_user.id,
                title=item.get("title", "Imported Item")[:200],
                url=item.get("url"),
                content_text=item.get("content_text") or item.get("description"),
                content_type=item.get("content_type", "link")
            )
            db.add(content_item)
            imported += 1

            if item.get("url"):
                existing_urls.add(item["url"])

        except Exception as e:
            errors.append(f"Error importing {item.get('title', 'item')}: {str(e)}")

    db.commit()

    return ImportResult(
        success=len(errors) == 0,
        items_imported=imported,
        items_skipped=skipped,
        errors=errors[:10]  # Limit error messages
    )

def _parse_import_file(filename: str, content: bytes) -> List[dict]:
    """Parse import file based on format"""
    items = []

    try:
        if filename.endswith(".json"):
            data = json.loads(content.decode("utf-8"))
            # Handle our export format
            if "content" in data:
                items = data["content"]
            # Handle Pocket export format
            elif isinstance(data, list):
                items = [{"title": i.get("title", ""), "url": i.get("url", "")} for i in data]

        elif filename.endswith(".csv"):
            reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
            items = list(reader)

        elif filename.endswith(".html"):
            # Parse bookmark HTML (Pocket, Instapaper format)
            import re
            links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]*)</a>', content.decode("utf-8"), re.IGNORECASE)
            items = [{"url": url, "title": title or url} for url, title in links]

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    return items

@router.post("/bulk/tag")
def bulk_add_tag(
    content_ids: List[int],
    tag_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a tag to multiple content items"""
    # Get or create tag
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)

    # Add tag to all specified content
    contents = db.query(Content).filter(
        Content.id.in_(content_ids),
        Content.user_id == current_user.id
    ).all()

    updated = 0
    for content in contents:
        if tag not in content.tags:
            content.tags.append(tag)
            updated += 1

    db.commit()

    return {"updated": updated, "tag": tag_name}

@router.delete("/bulk/delete")
def bulk_delete(
    content_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete multiple content items"""
    deleted = db.query(Content).filter(
        Content.id.in_(content_ids),
        Content.user_id == current_user.id
    ).delete(synchronize_session=False)

    db.commit()

    return {"deleted": deleted}
