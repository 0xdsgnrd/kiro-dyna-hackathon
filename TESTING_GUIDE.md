# Phase 2 Manual Testing Guide

## Prerequisites

1. **Backend Running**: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
2. **Frontend Running**: `cd frontend && npm run dev`
3. **Clean Database**: Optional - delete `backend/app.db` for fresh start

## Test Scenarios

### 1. Authentication Flow (Prerequisite)

**Register New User:**
- Navigate to http://localhost:3000
- Click "Get Started" or "Sign In"
- Click "Sign up here"
- Fill in:
  - Email: test@example.com
  - Username: testuser
  - Password: password123
- Submit → Should redirect to dashboard

**Login:**
- If already registered, login with credentials
- Should see dashboard with welcome message

---

### 2. Dashboard (Initial State)

**Expected:**
- ✅ User info displayed (username, email, member since)
- ✅ Statistics show 0 items, 0 tags, 0 categories
- ✅ "No content yet" message
- ✅ "Add Content" button visible
- ✅ "My Content" button in nav
- ✅ "Logout" button in nav

**Test:**
- Click "My Content" → Should go to /content
- Should see empty state with "Add Content" button

---

### 3. Create First Content Item

**Navigate to Add Content:**
- From dashboard or content list, click "Add Content"
- Should be at /content/add

**Fill Form:**
- Title: "My First Article" (required)
- Content Type: Article (default)
- URL: https://example.com
- Content/Notes: "This is my first content item for testing"
- Category: Leave empty (no categories yet)
- Tags: Leave empty (no tags yet)

**Submit:**
- Click "Create Content"
- ✅ Should see "Creating..." button text
- ✅ Should see success message
- ✅ Should redirect to /content after ~1.5 seconds

**Verify:**
- Should see 1 content card
- Card shows: 📄 icon, title, text preview, date
- Card has View/Edit/Delete buttons

---

### 4. Create Category

**Navigate to Add Content:**
- Click "Add Content" button

**Create Category (via backend API):**
Since we don't have a category management UI yet, we'll create via the add form:
- For now, skip category testing or use backend test script

**Alternative - Use Backend Test Script:**
```bash
cd backend
python3 test_content_api.py
```
This will create test categories and tags.

---

### 5. Create Content with Tags

**Navigate to Add Content:**
- Click "Add Content"

**Create Tags:**
- In "Tags" section, type "python" in input
- Click "Add Tag" or press Enter
- ✅ Tag should appear as a button
- ✅ Tag should be selected (blue background)
- Add more tags: "tutorial", "fastapi"

**Fill Form:**
- Title: "FastAPI Tutorial"
- Content Type: Article
- URL: https://fastapi.tiangolo.com
- Content: "Learn how to build modern APIs with FastAPI"
- Tags: Select all 3 tags created

**Submit:**
- ✅ Success message appears
- ✅ Redirects to content list

**Verify:**
- Should see 2 content items
- New item shows tags: #python #tutorial #fastapi

---

### 6. Search Content

**On Content List Page:**
- Type "FastAPI" in search box
- Click "Search" or press Enter
- ✅ Should show only matching content
- ✅ Should see "Clear" button

**Clear Search:**
- Click "Clear" button
- ✅ Should show all content again

**Test No Results:**
- Search for "nonexistent"
- ✅ Should show empty results (no cards)

---

### 7. View Content Detail

**From Content List:**
- Click "View" button on any content card
- Should navigate to /content/[id]

**Verify Detail Page:**
- ✅ Shows type icon and title
- ✅ Shows creation date
- ✅ Shows URL (if present) as clickable link
- ✅ Shows content text in gray box
- ✅ Shows tags with blue badges
- ✅ Shows category (if present)
- ✅ Has "Edit" and "Delete" buttons
- ✅ Has "Back to content" link

**Test URL Link:**
- If URL present, click it
- ✅ Should open in new tab

---

### 8. Edit Content

**From Detail Page:**
- Click "Edit" button
- Should navigate to /content/[id]/edit

**Verify Edit Form:**
- ✅ All fields pre-filled with existing data
- ✅ Tags are selected (blue)
- ✅ Category is selected (if present)

**Modify Content:**
- Change title to "FastAPI Tutorial - Updated"
- Add new tag: "backend"
- Modify content text

**Submit:**
- Click "Save Changes"
- ✅ Should see "Saving..." button text
- ✅ Should see success message
- ✅ Should redirect to detail page

**Verify Changes:**
- ✅ Title updated
- ✅ New tag appears
- ✅ Content text updated
- ✅ "Updated" date shown

---

### 9. Delete Content

**From Content List:**
- Click "Delete" button on a content card
- ✅ Should see confirmation dialog
- Click "Cancel" → Nothing happens
- Click "Delete" again → Click "OK"
- ✅ Card should disappear immediately

**From Detail Page:**
- Navigate to a content detail page
- Click "Delete" button
- ✅ Confirmation dialog appears
- Click "OK"
- ✅ Should redirect to /content list

---

### 10. Dashboard with Content

**Navigate to Dashboard:**
- Click browser back or go to /dashboard

**Verify Statistics:**
- ✅ Shows correct count of content items
- ✅ Shows count of unique tags used
- ✅ Shows count of categories (if any)

**Verify Recent Content:**
- ✅ Shows up to 5 most recent items
- ✅ Each item shows: icon, title, date, tags
- ✅ Items are clickable → Navigate to detail
- ✅ "View all content →" link at bottom

**Test Navigation:**
- Click on a recent content item
- ✅ Should navigate to detail page

---

### 11. Responsive Design

**Desktop (1920px):**
- ✅ Content list shows 3 columns
- ✅ Forms are centered with max-width
- ✅ Dashboard stats in 3 columns

**Tablet (768px):**
- ✅ Content list shows 2 columns
- ✅ Forms remain readable
- ✅ Dashboard stats in 3 columns

**Mobile (375px):**
- ✅ Content list shows 1 column
- ✅ Forms stack vertically
- ✅ Dashboard stats stack vertically
- ✅ Buttons remain accessible
- ✅ Navigation buttons visible

**Test:**
- Open browser DevTools
- Toggle device toolbar
- Test at 320px, 375px, 768px, 1920px

---

### 12. Error Handling

**Test Invalid Token:**
- Logout
- Manually navigate to /content
- ✅ Should redirect to /login

**Test Network Error:**
- Stop backend server
- Try to create content
- ✅ Should show error message
- ✅ Form should remain filled
- ✅ Can retry after restarting backend

**Test Validation:**
- Try to submit form without title
- ✅ Browser validation should prevent submit
- ✅ "Title is required" message may appear

---

### 13. Multiple Content Types

**Create Different Types:**
- Create content with type "Video" 🎥
- Create content with type "Note" 📝
- Create content with type "Link" 🔗

**Verify:**
- ✅ Each shows correct icon
- ✅ All types display correctly in list
- ✅ All types work in detail view

---

### 14. Tag Reuse

**Create New Content:**
- Navigate to /content/add
- ✅ Previously created tags should appear
- ✅ Can select existing tags
- ✅ Can create new tags
- ✅ Can mix existing and new tags

---

### 15. Logout and Re-login

**Logout:**
- Click "Logout" button
- ✅ Should redirect to home page
- ✅ Token cleared from localStorage

**Try to Access Protected Route:**
- Navigate to /content
- ✅ Should redirect to /login

**Login Again:**
- Login with same credentials
- ✅ Should see all previously created content
- ✅ Dashboard shows correct stats

---

## Test Results Checklist

### Core Functionality
- [ ] User can register and login
- [ ] Dashboard displays correctly
- [ ] Can create content with all fields
- [ ] Can create and select tags
- [ ] Can search content
- [ ] Can view content detail
- [ ] Can edit content
- [ ] Can delete content (with confirmation)
- [ ] Recent content shows on dashboard
- [ ] Statistics calculate correctly

### UI/UX
- [ ] Loading states show during operations
- [ ] Success messages appear
- [ ] Error messages appear for failures
- [ ] Confirmation dialogs work
- [ ] Navigation works correctly
- [ ] Back buttons work
- [ ] Responsive on mobile (320px+)
- [ ] Responsive on tablet (768px+)
- [ ] Responsive on desktop (1920px+)

### Data Integrity
- [ ] Content persists after page reload
- [ ] Tags persist and can be reused
- [ ] Search returns correct results
- [ ] Edit updates correctly
- [ ] Delete removes content
- [ ] User isolation works (can't see other users' content)

### Edge Cases
- [ ] Empty states display correctly
- [ ] No results found displays correctly
- [ ] Long titles truncate properly
- [ ] Long content text truncates in cards
- [ ] Multiple tags display correctly
- [ ] Forms handle missing optional fields

---

## Known Issues / Limitations

1. **No Category Management UI**: Categories must be created via API or test script
2. **No Pagination UI**: Shows all content (limit 50)
3. **No Sort Options**: Content ordered by creation date (backend default)
4. **No Filter by Type/Category**: Only text search implemented
5. **No Bulk Operations**: Must delete one at a time

These are acceptable for MVP and can be addressed in FEAT-009 or future iterations.

---

## Quick Test Script

For rapid testing, run the backend test script:

```bash
cd backend
python3 test_content_api.py
```

This will:
- Create a test user
- Create a category
- Create tags
- Create sample content
- Test all CRUD operations

Then verify in the frontend UI that the data appears correctly.
