# Quick Testing Reference

## Start Servers

**Backend (Terminal 1):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```
→ http://localhost:8000 (API)  
→ http://localhost:8000/docs (Swagger UI)

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```
→ http://localhost:3000

## Quick Test Flow

1. **Register**: http://localhost:3000 → Sign up
2. **Add Content**: Dashboard → "Add Content" button
3. **Create Tags**: In add form, type tag name → "Add Tag"
4. **Submit**: Fill title + type → "Create Content"
5. **View List**: Should see content card
6. **Search**: Type in search box → "Search"
7. **View Detail**: Click "View" button
8. **Edit**: Click "Edit" button → Modify → "Save Changes"
9. **Delete**: Click "Delete" → Confirm

## Test Data Script

```bash
cd backend
python3 test_content_api.py
```

Creates:
- Test user (testuser / password123)
- Sample category
- Sample tags (python, fastapi, tutorial)
- Sample content item

## Check Status

```bash
./test-phase2.sh
```

Shows:
- Backend status
- Frontend status
- Testing checklist

## Key URLs

- **Home**: http://localhost:3000
- **Login**: http://localhost:3000/login
- **Dashboard**: http://localhost:3000/dashboard
- **Content List**: http://localhost:3000/content
- **Add Content**: http://localhost:3000/content/add
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Common Issues

**Backend won't start:**
- Check virtual environment activated
- Check port 8000 not in use: `lsof -i :8000`
- Check requirements installed: `pip install -r requirements.txt`

**Frontend won't start:**
- Check node_modules installed: `npm install`
- Check port 3000 not in use: `lsof -i :3000`
- Check .env.local exists with API URL

**Can't login:**
- Check backend is running
- Check CORS allows localhost:3000
- Check browser console for errors

**No content showing:**
- Check JWT token in localStorage
- Check backend logs for errors
- Try creating new content

## Testing Checklist

Quick checklist for manual testing:

- [ ] Register new user
- [ ] Login works
- [ ] Dashboard shows stats
- [ ] Can add content
- [ ] Can create tags
- [ ] Can search content
- [ ] Can view detail
- [ ] Can edit content
- [ ] Can delete content
- [ ] Responsive on mobile
- [ ] No console errors

## Full Documentation

- **TESTING_GUIDE.md** - Comprehensive testing scenarios
- **PHASE2_COMPLETE.md** - Full development summary
- **API_REFERENCE.md** - API endpoint documentation

## Report Issues

If you find bugs during testing:
1. Note the steps to reproduce
2. Check browser console for errors
3. Check backend terminal for errors
4. Document expected vs actual behavior

---

**Ready to test!** Start both servers and open http://localhost:3000
