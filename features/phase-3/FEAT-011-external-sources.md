# [FEAT-011] External Content Sources

## Goal
Enable automatic content aggregation from external sources like RSS feeds and web scraping to reduce manual content entry.

## Description
Currently, users must manually add all content items. This creates friction and limits the platform's value as a content aggregation tool. By integrating with external sources, users can automatically collect content from their favorite blogs, news sites, and other sources, transforming the platform from a manual content manager into a true aggregation system.

---

## Requirements
Enable users to configure and manage external content sources that automatically import new content.

- RSS feed integration with automatic fetching
- Web scraping for article metadata extraction
- Background job system for scheduled content imports
- Duplicate detection to prevent content duplication
- Content source management (add, edit, delete, pause)
- Manual import trigger for immediate content fetching
- Content preview and approval workflow
- Error handling and retry logic for failed imports

Content should be normalized into the existing content model with proper attribution to sources.

### Non-Goals
- Real-time content streaming or WebSocket updates
- Advanced web scraping with JavaScript rendering
- Social media API integrations (Twitter, Facebook)
- Content modification or editing during import

---

## Acceptance Criteria

- [x] Users can add RSS feed URLs through a management interface
- [x] Background jobs automatically fetch new content every hour
- [x] Imported content includes title, description, URL, and publication date
- [x] Duplicate content is detected and skipped based on URL matching
- [x] Users can manually trigger import for immediate content fetching
- [x] Failed imports are logged with error details and retry automatically
- [x] Content sources can be paused, resumed, or deleted
- [x] Imported content is properly attributed to its source

---

## Technical Context

**Backend Architecture:**
- Use FastAPI Background Tasks for job scheduling (avoid Celery complexity for MVP)
- aiohttp for async HTTP requests to external sources
- feedparser library for RSS parsing
- BeautifulSoup for basic web scraping
- SQLAlchemy models for content sources and import logs

**Database Schema:**
- ContentSource model (url, type, last_fetched, active, error_count)
- ImportLog model (source_id, status, items_imported, error_message)
- Add source_id foreign key to Content model

**Performance Considerations:**
- Rate limiting for external requests (1 request per second per source)
- Timeout handling (30 second max per request)
- Batch processing for multiple content items

---

## Risks / Open Questions
- RSS feeds may be unreliable or change format unexpectedly
- Web scraping may break when target sites change structure
- Background job failures could accumulate without proper monitoring
- Large RSS feeds might overwhelm the system with too many items

---

## Dependencies
- Phase 2 content management system must be complete
- No external service dependencies (self-contained solution)

---

## Success Metrics
- Successfully import content from at least 3 different RSS feeds
- Background jobs run reliably with <5% failure rate
- Duplicate detection accuracy >95%
- Import processing time <30 seconds per source

---

## Definition of Done
- All acceptance criteria met
- Background job system tested with multiple concurrent sources
- Error handling tested with invalid/unreachable URLs
- Database migration script for new models
- API documentation updated with new endpoints
