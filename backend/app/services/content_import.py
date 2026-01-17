import asyncio
import aiohttp
import feedparser
from datetime import datetime, timezone
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.content_source import ContentSource, ImportLog
from app.models.content import Content
from app.models.user import User

class ContentImportService:
    def __init__(self, db: Session):
        self.db = db
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def import_from_source(self, source_id: int) -> Dict:
        """Import content from a single source"""
        source = self.db.query(ContentSource).filter(ContentSource.id == source_id).first()
        if not source or not source.active:
            return {"status": "error", "message": "Source not found or inactive"}
        
        # Create import log
        import_log = ImportLog(
            source_id=source_id,
            status="running",
            started_at=datetime.now(timezone.utc)
        )
        self.db.add(import_log)
        self.db.commit()
        
        try:
            if source.source_type == "rss":
                result = await self._import_rss(source, import_log)
            elif source.source_type == "webpage":
                result = await self._import_webpage(source, import_log)
            else:
                result = {"status": "error", "message": "Unknown source type"}
            
            # Update source
            source.last_fetched = datetime.now(timezone.utc)
            if result["status"] == "success":
                source.error_count = 0
                source.last_error = None
            else:
                source.error_count += 1
                source.last_error = result.get("message", "Unknown error")
            
            # Update import log
            import_log.status = result["status"]
            import_log.items_imported = result.get("items_imported", 0)
            import_log.items_skipped = result.get("items_skipped", 0)
            import_log.error_message = result.get("message") if result["status"] == "error" else None
            import_log.completed_at = datetime.now(timezone.utc)
            
            self.db.commit()
            return result
            
        except Exception as e:
            import_log.status = "error"
            import_log.error_message = str(e)
            import_log.completed_at = datetime.now(timezone.utc)
            source.error_count += 1
            source.last_error = str(e)
            self.db.commit()
            return {"status": "error", "message": str(e)}
    
    async def _import_rss(self, source: ContentSource, import_log: ImportLog) -> Dict:
        """Import content from RSS feed"""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            try:
                async with session.get(source.url) as response:
                    if response.status != 200:
                        return {"status": "error", "message": f"HTTP {response.status}"}
                    
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    if feed.bozo:
                        return {"status": "error", "message": "Invalid RSS feed"}
                    
                    items_imported = 0
                    items_skipped = 0
                    
                    for entry in feed.entries[:20]:  # Limit to 20 items per import
                        if self._content_exists(entry.link, source.user_id):
                            items_skipped += 1
                            continue
                        
                        content_item = Content(
                            user_id=source.user_id,
                            source_id=source.id,
                            title=entry.title[:200],
                            url=entry.link,
                            content_text=self._extract_description(entry),
                            content_type="article"
                        )
                        
                        self.db.add(content_item)
                        items_imported += 1
                    
                    return {
                        "status": "success",
                        "items_imported": items_imported,
                        "items_skipped": items_skipped
                    }
                    
            except asyncio.TimeoutError:
                return {"status": "error", "message": "Request timeout"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    async def _import_webpage(self, source: ContentSource, import_log: ImportLog) -> Dict:
        """Import content from webpage (basic metadata extraction)"""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            try:
                async with session.get(source.url) as response:
                    if response.status != 200:
                        return {"status": "error", "message": f"HTTP {response.status}"}
                    
                    if self._content_exists(source.url, source.user_id):
                        return {"status": "success", "items_imported": 0, "items_skipped": 1}
                    
                    html = await response.text()
                    title = self._extract_title(html)
                    description = self._extract_meta_description(html)
                    
                    content_item = Content(
                        user_id=source.user_id,
                        source_id=source.id,
                        title=title[:200] if title else source.name,
                        url=source.url,
                        content_text=description,
                        content_type="link"
                    )
                    
                    self.db.add(content_item)
                    return {"status": "success", "items_imported": 1, "items_skipped": 0}
                    
            except asyncio.TimeoutError:
                return {"status": "error", "message": "Request timeout"}
            except Exception as e:
                return {"status": "error", "message": str(e)}
    
    def _content_exists(self, url: str, user_id: int) -> bool:
        """Check if content with URL already exists for user"""
        return self.db.query(Content).filter(
            Content.url == url,
            Content.user_id == user_id
        ).first() is not None
    
    def _extract_description(self, entry) -> Optional[str]:
        """Extract description from RSS entry"""
        if hasattr(entry, 'description'):
            return entry.description[:500]
        elif hasattr(entry, 'summary'):
            return entry.summary[:500]
        return None
    
    def _extract_title(self, html: str) -> Optional[str]:
        """Extract title from HTML"""
        import re
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_meta_description(self, html: str) -> Optional[str]:
        """Extract meta description from HTML"""
        import re
        match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        return match.group(1).strip() if match else None
