# [FEAT-007] Backend Content Service (Core CRUD)

## Goal
Implement backend models, schemas, and API endpoints for content management with full CRUD operations, tagging, and categorization.

## Description
Build the backend foundation for content aggregation by creating database models, Pydantic schemas, and RESTful API endpoints. This includes content items, tags, categories, and the relationships between them.

---

## Requirements

- **Content Model**: Store content items with title, URL, text, type, timestamps
- **Tag System**: Many-to-many relationship between content and tags
- **Category System**: One-to-many relationship (content belongs to one category)
- **CRUD Endpoints**: Create, read, update, delete for content, tags, categories
- **Authentication**: All endpoints protected with JWT authentication
- **User Isolation**: Users can only access their own content
- **Search**: Basic search by title, content text, and tags
- **Pagination**: Support for paginated content lists

### Non-Goals
- Full-text search (use simple LIKE queries for MVP)
- Content preview generation
- External API integrations
- Content import/export

---

## Acceptance Criteria

- [x] Content model created with all required fields
- [x] Tag and Category models created with relationships
- [x] ContentCreate, ContentUpdate, ContentResponse schemas defined
- [x] POST /api/v1/content endpoint creates content (protected)
- [x] GET /api/v1/content endpoint lists user's content with pagination (protected)
- [x] GET /api/v1/content/{id} endpoint returns single content item (protected)
- [x] PUT /api/v1/content/{id} endpoint updates content (protected)
- [x] DELETE /api/v1/content/{id} endpoint deletes content (protected)
- [x] GET /api/v1/content/search?q={query} endpoint searches content (protected)
- [x] Tag CRUD endpoints implemented (create, list, delete)
- [x] Category CRUD endpoints implemented (create, list, update, delete)
- [x] Authentication dependency enforces user isolation
- [x] Database migrations run successfully
- [x] All endpoints documented in API_REFERENCE.md

---

## Technical Context

**Database Schema:**
```python
# Content Model
- id: Integer (PK)
- user_id: Integer (FK to users)
- title: String(200)
- url: String(500), nullable
- content_text: Text, nullable
- content_type: String(50) # article, video, note, link
- created_at: DateTime
- updated_at: DateTime
- tags: relationship (many-to-many)
- category_id: Integer (FK to categories), nullable

# Tag Model
- id: Integer (PK)
- name: String(50), unique
- created_at: DateTime

# Category Model
- id: Integer (PK)
- name: String(100)
- description: String(500), nullable
- user_id: Integer (FK to users)
- created_at: DateTime
```

**Authentication Dependency:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode JWT and return user
    # Raise 401 if invalid
```

---

## Risks / Open Questions

- **Search Performance**: Simple LIKE queries may be slow with large datasets (acceptable for MVP)
- **Tag Uniqueness**: Should tags be global or per-user? (Decision: global for simplicity)

---

## Dependencies

- Phase 1 complete (authentication system)
- SQLAlchemy models and session configured
- JWT authentication working

---

## Implementation Steps

1. Create `backend/app/models/content.py` with Content model
2. Create `backend/app/models/tag.py` with Tag model and association table
3. Create `backend/app/models/category.py` with Category model
4. Create `backend/app/schemas/content.py` with all schemas
5. Create `backend/app/api/deps.py` with `get_current_user` dependency
6. Create `backend/app/api/routes/content.py` with content endpoints
7. Create `backend/app/api/routes/tags.py` with tag endpoints
8. Create `backend/app/api/routes/categories.py` with category endpoints
9. Update `backend/app/main.py` to register new routers
10. Test all endpoints with curl/Postman
11. Update API_REFERENCE.md

---

## Definition of Done

- All acceptance criteria met
- All endpoints return correct status codes
- User isolation enforced (users can't access others' content)
- Database relationships working correctly
- API documentation updated
- Manual testing complete
