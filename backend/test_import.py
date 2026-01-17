#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.content_import import ContentImportService
from app.db.session import SessionLocal
from app.models.content_source import ContentSource
from app.models.user import User

async def test_rss_import():
    """Test RSS import functionality"""
    db = SessionLocal()
    
    try:
        # Create test user if not exists
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            user = User(
                email="test@example.com",
                username="testuser",
                hashed_password="dummy"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create test RSS source
        source = ContentSource(
            user_id=user.id,
            name="Test RSS Feed",
            url="https://feeds.feedburner.com/oreilly/radar",  # O'Reilly Radar RSS
            source_type="rss",
            active=True
        )
        db.add(source)
        db.commit()
        db.refresh(source)
        
        print(f"Created test source: {source.name}")
        
        # Test import
        import_service = ContentImportService(db)
        result = await import_service.import_from_source(source.id)
        
        print(f"Import result: {result}")
        
        # Clean up
        db.delete(source)
        db.commit()
        
        return result["status"] == "success"
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_rss_import())
    print(f"✅ RSS import test: {'PASSED' if success else 'FAILED'}")
