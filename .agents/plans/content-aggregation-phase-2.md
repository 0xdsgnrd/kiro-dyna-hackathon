# Feature: Content Aggregation Platform - Phase 2: Content Aggregation Features

## Feature Description

Extend the content aggregation platform with core content management capabilities, allowing users to add, organize, search, and manage content items from various sources. This phase builds on the authentication foundation from Phase 1 to deliver the primary value proposition of the platform.

## User Story

As an authenticated user
I want to add content items from various sources, organize them with tags and categories, and search through my collection
So that I can efficiently manage and access all my aggregated content in one centralized location

## Problem Statement

With authentication complete (Phase 1), users need the ability to:
- Add content items (URLs, text snippets, notes) to their collection
- Organize content with tags and categories
- Search and filter their content collection
- View content in an organized dashboard
- Edit and delete content items

Currently, the platform only supports user authentication but has no content management capabilities.

## Solution Statement

Build content management features with:
- **Backend**: Content service with CRUD operations, tagging system, search functionality
- **Frontend**: Content dashboard, add/edit forms, search interface, tag management
- **Database**: Content storage with relationships to users, tags, and categories
- **API**: RESTful endpoints for content operations

---

## CONTEXT REFERENCES

### Existing Foundation (Phase 1)

**Completed:**
- ✅ User authentication with JWT
- ✅ User registration and login
- ✅ Protected dashboard
- ✅ Backend: FastAPI with SQLAlchemy
- ✅ Frontend: Next.js with TypeScript and Tailwind CSS
- ✅ Test infrastructure (95% backend, 79.6% frontend coverage)

**Architecture:**
```
Frontend (Next.js) → API → User Service (FastAPI) → Database (SQLite)
```

### Technical Stack

- **Backend**: FastAPI 0.115+, SQLAlchemy 2.0+, Pydantic 2.10+
- **Frontend**: Next.js 16.1.1, React 19.2.3, TypeScript 5+, Tailwind CSS 4
- **Database**: SQLite (dev), PostgreSQL (production)
- **Authentication**: JWT tokens (already implemented)

### Relevant Documentation

- [FastAPI CRUD Operations](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Next.js Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [React Hook Form](https://react-hook-form.com/) (for form management)

---

## IMPLEMENTATION PLAN

### Phase 2.1: Backend Content Service (Core CRUD)

**Objective**: Implement backend models, schemas, and API endpoints for content management

**Tasks:**

1. **Create Content Models** (`backend/app/models/content.py`)
   - Content model: id, user_id, title, url, content_text, content_type, created_at, updated_at
   - Tag model: id, name, created_at
   - ContentTag association table (many-to-many relationship)
   - Category model: id, name, description, user_id

2. **Create Content Schemas** (`backend/app/schemas/content.py`)
   - ContentCreate: title, url?, content_text?, content_type, tag_ids?, category_id?
   - ContentUpdate: title?, url?, content_text?, tag_ids?, category_id?
   - ContentResponse: all fields + tags + category + user info
   - TagCreate/TagResponse
   - CategoryCreate/CategoryResponse

3. **Create Content Routes** (`backend/app/api/routes/content.py`)
   - POST /api/v1/content - Create content item (protected)
   - GET /api/v1/content - List user's content (protected, with pagination)
   - GET /api/v1/content/{id} - Get single content item (protected)
   - PUT /api/v1/content/{id} - Update content item (protected)
   - DELETE /api/v1/content/{id} - Delete content item (protected)
   - GET /api/v1/content/search?q={query} - Search content (protected)

4. **Create Tag Routes** (`backend/app/api/routes/tags.py`)
   - POST /api/v1/tags - Create tag (protected)
   - GET /api/v1/tags - List all tags (protected)
   - DELETE /api/v1/tags/{id} - Delete tag (protected)

5. **Create Category Routes** (`backend/app/api/routes/categories.py`)
   - POST /api/v1/categories - Create category (protected)
   - GET /api/v1/categories - List user's categories (protected)
   - PUT /api/v1/categories/{id} - Update category (protected)
   - DELETE /api/v1/categories/{id} - Delete category (protected)

6. **Add Authentication Dependency**
   - Create `get_current_user` dependency using JWT token
   - Protect all content routes with authentication
   - Ensure users can only access their own content

**Validation:**
```bash
# Test content CRUD
curl -X POST http://localhost:8000/api/v1/content \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Article","url":"https://example.com","content_type":"article"}'

# Test search
curl http://localhost:8000/api/v1/content/search?q=test \
  -H "Authorization: Bearer $TOKEN"
```

**Files to Create:**
- `backend/app/models/content.py`
- `backend/app/models/tag.py`
- `backend/app/models/category.py`
- `backend/app/schemas/content.py`
- `backend/app/api/routes/content.py`
- `backend/app/api/routes/tags.py`
- `backend/app/api/routes/categories.py`
- `backend/app/api/deps.py` (authentication dependency)

**Files to Modify:**
- `backend/app/main.py` (register new routers)
- `backend/app/db/session.py` (ensure new tables are created)

---

### Phase 2.2: Frontend Content Management UI

**Objective**: Build user interface for adding, viewing, and managing content

**Tasks:**

1. **Create Content API Client** (`frontend/lib/content-api.ts`)
   - createContent(data, token)
   - getContent(id, token)
   - listContent(token, page?, limit?)
   - updateContent(id, data, token)
   - deleteContent(id, token)
   - searchContent(query, token)

2. **Create Content Types** (`frontend/lib/types.ts`)
   - Content interface
   - Tag interface
   - Category interface
   - ContentFormData interface

3. **Create Content Context** (`frontend/contexts/ContentContext.tsx`)
   - Manage content state
   - Provide CRUD operations
   - Handle loading and error states

4. **Create Add Content Page** (`frontend/app/content/add/page.tsx`)
   - Form with title, URL, content text, content type
   - Tag selection/creation
   - Category selection
   - Submit to API
   - Redirect to content list on success

5. **Create Content List Page** (`frontend/app/content/page.tsx`)
   - Display user's content in cards/list
   - Pagination controls
   - Search bar
   - Filter by tags/categories
   - Edit and delete buttons

6. **Create Content Detail Page** (`frontend/app/content/[id]/page.tsx`)
   - Display full content details
   - Show tags and category
   - Edit and delete buttons
   - Back to list button

7. **Create Edit Content Page** (`frontend/app/content/[id]/edit/page.tsx`)
   - Pre-filled form with existing content
   - Update functionality
   - Cancel button

8. **Update Dashboard** (`frontend/app/dashboard/page.tsx`)
   - Add "Add Content" button
   - Show recent content items (5 most recent)
   - Link to full content list
   - Show content statistics (total items, tags, categories)

**Validation:**
```bash
# Build and check for errors
cd frontend && npm run build

# Run tests
npm test
```

**Files to Create:**
- `frontend/lib/content-api.ts`
- `frontend/contexts/ContentContext.tsx`
- `frontend/app/content/page.tsx`
- `frontend/app/content/add/page.tsx`
- `frontend/app/content/[id]/page.tsx`
- `frontend/app/content/[id]/edit/page.tsx`
- `frontend/components/ContentCard.tsx`
- `frontend/components/ContentForm.tsx`
- `frontend/components/SearchBar.tsx`
- `frontend/components/TagSelector.tsx`

**Files to Modify:**
- `frontend/lib/types.ts` (add content types)
- `frontend/app/dashboard/page.tsx` (add content overview)
- `frontend/app/layout.tsx` (wrap with ContentProvider if needed)

---

### Phase 2.3: Search and Filtering

**Objective**: Implement search functionality and filtering options

**Tasks:**

1. **Backend Search Implementation**
   - Add search query to content list endpoint
   - Implement SQLAlchemy filters for title, content_text, tags
   - Add filter by category
   - Add filter by content_type
   - Add sorting options (date, title)

2. **Frontend Search UI**
   - Search bar component with debouncing
   - Filter dropdowns (category, content type)
   - Tag filter chips
   - Sort dropdown
   - Clear filters button

3. **Search Results Display**
   - Highlight search terms in results
   - Show match count
   - Empty state for no results
   - Loading state during search

**Validation:**
```bash
# Test search with various queries
curl "http://localhost:8000/api/v1/content/search?q=test&category=1&content_type=article" \
  -H "Authorization: Bearer $TOKEN"
```

**Files to Modify:**
- `backend/app/api/routes/content.py` (enhance search)
- `frontend/app/content/page.tsx` (add search/filter UI)
- `frontend/components/SearchBar.tsx` (add debouncing)

---

### Phase 2.4: Testing and Validation

**Objective**: Ensure all content features are thoroughly tested

**Tasks:**

1. **Backend Tests** (`backend/tests/test_content.py`)
   - Test content CRUD operations
   - Test authentication on protected routes
   - Test user isolation (users can't access others' content)
   - Test search functionality
   - Test tag and category operations
   - Target: 85%+ coverage for content service

2. **Frontend Tests** (`frontend/__tests__/content.test.ts`)
   - Test content API client functions
   - Test ContentContext operations
   - Test form validation
   - Target: 75%+ coverage for content features

3. **Integration Testing**
   - Test full flow: login → add content → view → edit → delete
   - Test search and filtering
   - Test tag management

4. **Update Documentation**
   - Update README with content features
   - Update API_REFERENCE.md with new endpoints
   - Create CONTENT_USAGE.md guide

**Validation:**
```bash
# Backend tests
cd backend && pytest tests/test_content.py -v --cov=app

# Frontend tests
cd frontend && npm test -- content.test.ts

# Full test suite
cd backend && pytest tests/ -v --cov=app
cd frontend && npm test
```

**Files to Create:**
- `backend/tests/test_content.py`
- `backend/tests/test_tags.py`
- `backend/tests/test_categories.py`
- `frontend/__tests__/content.test.ts`
- `frontend/__tests__/content-api.test.ts`
- `CONTENT_USAGE.md`

**Files to Modify:**
- `README.md` (add content features section)
- `backend/API_REFERENCE.md` (document new endpoints)

---

## SUCCESS CRITERIA

### Functional Requirements

- ✅ Users can create content items with title, URL, text, and type
- ✅ Users can view all their content in a paginated list
- ✅ Users can edit and delete their own content
- ✅ Users can add tags to content items
- ✅ Users can create and manage categories
- ✅ Users can search content by title, text, or tags
- ✅ Users can filter content by category and type
- ✅ Dashboard shows content overview and statistics

### Technical Requirements

- ✅ Backend: 85%+ test coverage for content service
- ✅ Frontend: 75%+ test coverage for content features
- ✅ All API endpoints documented
- ✅ Authentication enforced on all content routes
- ✅ User isolation: users can only access their own content
- ✅ TypeScript: 0 errors, 0 warnings
- ✅ ESLint: 0 errors, 0 warnings
- ✅ Production build successful

### Performance Requirements

- ✅ Content list loads in < 500ms (for 100 items)
- ✅ Search returns results in < 300ms
- ✅ API response time < 200ms (p95)

### User Experience Requirements

- ✅ Intuitive content creation form
- ✅ Responsive design (mobile + desktop)
- ✅ Loading states for all async operations
- ✅ Error messages for failed operations
- ✅ Success feedback for completed actions

---

## FEATURE TICKETS

### FEAT-007: Backend Content Service (Core CRUD)
**Priority**: High  
**Estimated Time**: 3-4 hours  
**Dependencies**: Phase 1 complete  
**Description**: Implement backend models, schemas, and API endpoints for content CRUD operations

### FEAT-008: Frontend Content Management UI
**Priority**: High  
**Estimated Time**: 4-5 hours  
**Dependencies**: FEAT-007  
**Description**: Build user interface for adding, viewing, editing, and deleting content

### FEAT-009: Search and Filtering
**Priority**: Medium  
**Estimated Time**: 2-3 hours  
**Dependencies**: FEAT-007, FEAT-008  
**Description**: Implement search functionality and filtering options for content

### FEAT-010: Content Testing and Documentation
**Priority**: High  
**Estimated Time**: 2-3 hours  
**Dependencies**: FEAT-007, FEAT-008, FEAT-009  
**Description**: Comprehensive testing and documentation for content features

**Total Estimated Time**: 11-15 hours

---

## RISKS AND MITIGATION

### Risk 1: Database Performance with Large Content Collections
**Mitigation**: 
- Implement pagination from the start
- Add database indexes on frequently queried fields (user_id, created_at, title)
- Consider full-text search for production (PostgreSQL)

### Risk 2: Complex Tag Management
**Mitigation**:
- Start with simple tag creation and assignment
- Use many-to-many relationship for flexibility
- Implement tag autocomplete for better UX

### Risk 3: Search Performance
**Mitigation**:
- Use SQLAlchemy LIKE queries for MVP
- Add debouncing on frontend to reduce API calls
- Plan for full-text search upgrade in future

### Risk 4: User Isolation Security
**Mitigation**:
- Always filter by user_id in database queries
- Add tests specifically for user isolation
- Use FastAPI dependency injection for authentication

---

## FUTURE ENHANCEMENTS (Phase 3+)

- **Content Import**: Bulk import from RSS feeds, bookmarks, APIs
- **Content Sharing**: Share content items with other users
- **Collections**: Group content into collections/folders
- **Rich Text Editor**: Enhanced content editing with formatting
- **Content Preview**: Generate previews for URLs (title, image, description)
- **Analytics**: Track content views, popular tags, usage statistics
- **Export**: Export content to various formats (JSON, CSV, Markdown)
- **Mobile App**: Native mobile applications
- **Browser Extension**: Quick content capture from browser

---

## NOTES

- This plan builds directly on Phase 1 authentication foundation
- All features maintain the same code quality standards (95%+ backend, 75%+ frontend coverage)
- Architecture remains microservices-ready for future expansion
- Focus on MVP features first, then iterate based on user feedback
- Maintain comprehensive documentation throughout development
