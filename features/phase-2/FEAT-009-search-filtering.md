# [FEAT-009] Search and Filtering

## Goal
Implement search functionality and filtering options to help users find content quickly.

## Description
Add search capabilities to the content list page, allowing users to search by title, text, and tags. Include filters for category and content type, plus sorting options.

---

## Requirements

- **Search Bar**: Text input with debouncing (300ms)
- **Search Backend**: Query title, content_text, and tag names
- **Category Filter**: Dropdown to filter by category
- **Content Type Filter**: Dropdown to filter by type
- **Tag Filter**: Click tags to filter by tag
- **Sort Options**: Sort by date (newest/oldest) or title (A-Z/Z-A)
- **Clear Filters**: Button to reset all filters
- **Results Count**: Display number of results found
- **Empty State**: Show message when no results found
- **URL Parameters**: Persist search/filter state in URL

### Non-Goals
- Advanced search operators (AND, OR, NOT)
- Saved searches
- Search history
- Full-text search ranking

---

## Acceptance Criteria

- [ ] Search bar on content list page
- [ ] Search queries backend with 300ms debounce
- [ ] Search matches title, content_text, and tag names
- [ ] Category filter dropdown works correctly
- [ ] Content type filter dropdown works correctly
- [ ] Clicking tag filters by that tag
- [ ] Sort dropdown changes result order
- [ ] "Clear Filters" button resets all filters
- [ ] Results count displays correctly
- [ ] Empty state shows when no results
- [ ] Search/filter state persists in URL parameters
- [ ] Loading indicator shows during search
- [ ] Backend search endpoint returns results in < 300ms
- [ ] Frontend tests pass for search functionality

---

## Technical Context

**Backend Search Endpoint:**
```python
@router.get("/search")
def search_content(
    q: str = "",
    category_id: Optional[int] = None,
    content_type: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Build query with filters
    # Return paginated results
```

**Frontend Search Component:**
```typescript
// Debounced search
const [searchQuery, setSearchQuery] = useState('');
const debouncedSearch = useMemo(
  () => debounce((query: string) => {
    // Fetch results
  }, 300),
  []
);
```

**URL Parameters:**
```
/content?q=test&category=1&type=article&sort=created_at&order=desc
```

---

## Risks / Open Questions

- **Search Performance**: LIKE queries may be slow (acceptable for MVP, plan for full-text search later)
- **Debounce Timing**: 300ms may feel slow (test with users)

---

## Dependencies

- FEAT-007 (Backend Content Service) must be complete
- FEAT-008 (Frontend Content UI) must be complete

---

## Implementation Steps

1. Update `backend/app/api/routes/content.py` with search logic
2. Add SQLAlchemy filters for search query
3. Add filters for category_id and content_type
4. Add sorting logic
5. Create `frontend/components/SearchBar.tsx` with debouncing
6. Create `frontend/components/FilterBar.tsx` with dropdowns
7. Update `frontend/app/content/page.tsx` to use search/filters
8. Add URL parameter handling with Next.js router
9. Add empty state component
10. Test search performance with sample data

---

## Definition of Done

- All acceptance criteria met
- Search returns results quickly (< 300ms)
- Filters work correctly in combination
- URL parameters persist state
- Empty state displays correctly
- Tests pass for search functionality
