# [FEAT-008] Frontend Content Management UI

## Goal
Build user interface for adding, viewing, editing, and managing content items with tags and categories.

## Description
Create a complete content management interface including content list, add/edit forms, detail views, and dashboard integration. Users should be able to perform all CRUD operations on their content through an intuitive UI.

---

## Requirements

- **Content List Page**: Display all user's content in cards/list format
- **Add Content Form**: Form to create new content items
- **Edit Content Form**: Form to update existing content
- **Content Detail View**: Display full content details
- **Dashboard Integration**: Show recent content and statistics
- **Tag Management**: Select/create tags for content
- **Category Management**: Select category for content
- **Responsive Design**: Works on mobile and desktop
- **Loading States**: Show loading indicators for async operations
- **Error Handling**: Display error messages for failed operations

### Non-Goals
- Rich text editor (use textarea for MVP)
- Content preview generation
- Drag-and-drop organization
- Bulk operations

---

## Acceptance Criteria

- [x] Content list page at /content displays user's content
- [x] Pagination controls work correctly
- [x] Add content page at /content/add with form
- [x] Form validates required fields (title, content_type)
- [x] Content detail page at /content/[id] shows full details
- [x] Edit content page at /content/[id]/edit with pre-filled form
- [x] Delete button with confirmation dialog
- [x] Dashboard shows 5 most recent content items
- [x] Dashboard shows content statistics (total items, tags, categories)
- [x] Tag selector allows selecting existing tags
- [x] Category dropdown shows user's categories
- [x] All forms show loading state during submission
- [x] Error messages displayed for failed operations
- [x] Success messages displayed for completed actions
- [x] Responsive design works on mobile (320px+)
- [x] TypeScript compilation passes (0 errors)
- [x] ESLint passes (0 errors, 0 warnings)

---

## Technical Context

**Content API Client:**
```typescript
// frontend/lib/content-api.ts
export async function createContent(data: ContentFormData, token: string): Promise<Content>
export async function listContent(token: string, page?: number, limit?: number): Promise<ContentList>
export async function getContent(id: number, token: string): Promise<Content>
export async function updateContent(id: number, data: ContentFormData, token: string): Promise<Content>
export async function deleteContent(id: number, token: string): Promise<void>
```

**Content Types:**
```typescript
interface Content {
  id: number;
  title: string;
  url?: string;
  content_text?: string;
  content_type: 'article' | 'video' | 'note' | 'link';
  tags: Tag[];
  category?: Category;
  created_at: string;
  updated_at: string;
}

interface ContentFormData {
  title: string;
  url?: string;
  content_text?: string;
  content_type: string;
  tag_ids?: number[];
  category_id?: number;
}
```

**Page Structure:**
- `/content` - Content list with search and filters
- `/content/add` - Add new content form
- `/content/[id]` - Content detail view
- `/content/[id]/edit` - Edit content form

---

## Risks / Open Questions

- **Form Complexity**: Content form has many optional fields (keep UI simple)
- **Tag Creation**: Should users create tags inline or separately? (Decision: inline for better UX)

---

## Dependencies

- FEAT-007 (Backend Content Service) must be complete
- Authentication context working
- API client pattern established

---

## Design / Mockups

**Content List Page:**
- Grid of content cards (3 columns on desktop, 1 on mobile)
- Each card shows: title, type icon, first 100 chars of text, tags, date
- "Add Content" button in top right
- Search bar at top
- Pagination at bottom

**Add Content Form:**
- Title input (required)
- URL input (optional)
- Content text textarea (optional)
- Content type dropdown (required)
- Tag selector with autocomplete
- Category dropdown
- Submit and Cancel buttons

**Dashboard Integration:**
- "Recent Content" section with 5 items
- "Add Content" button
- Statistics: X items, Y tags, Z categories

---

## Definition of Done

- All acceptance criteria met
- All pages responsive and styled
- Forms validate correctly
- Loading and error states implemented
- TypeScript and ESLint pass
- Production build successful
- Manual testing complete on desktop and mobile
