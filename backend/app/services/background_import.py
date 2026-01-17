import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.content_source import ContentSource
from app.services.content_import import ContentImportService

class BackgroundImportService:
    def __init__(self):
        self.running = False
    
    async def start_scheduler(self):
        """Start the background import scheduler"""
        self.running = True
        while self.running:
            try:
                await self._run_scheduled_imports()
                # Wait 1 hour before next run
                await asyncio.sleep(3600)
            except Exception as e:
                print(f"Background import error: {e}")
                # Wait 5 minutes before retry on error
                await asyncio.sleep(300)
    
    def stop_scheduler(self):
        """Stop the background import scheduler"""
        self.running = False
    
    async def _run_scheduled_imports(self):
        """Run imports for all active sources that need updating"""
        db = SessionLocal()
        try:
            # Get sources that haven't been fetched in the last hour
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=1)
            
            sources = db.query(ContentSource).filter(
                ContentSource.active == True,
                (ContentSource.last_fetched.is_(None) | 
                 (ContentSource.last_fetched < cutoff_time)),
                ContentSource.error_count < 5  # Skip sources with too many errors
            ).all()
            
            if not sources:
                return
            
            print(f"Running scheduled imports for {len(sources)} sources")
            
            import_service = ContentImportService(db)
            
            # Process sources with rate limiting (1 per second)
            for source in sources:
                try:
                    result = await import_service.import_from_source(source.id)
                    print(f"Import from {source.name}: {result['status']}")
                    
                    # Rate limiting
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error importing from {source.name}: {e}")
                    
        finally:
            db.close()

# Global instance
background_service = BackgroundImportService()
