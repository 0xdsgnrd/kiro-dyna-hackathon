# API Reference

## Authentication Endpoints

### Register New User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2026-01-14T10:00:00"
}
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepass123"
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Content Endpoints

All content endpoints require authentication. Include the JWT token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Content
```bash
curl -X POST http://localhost:8000/api/v1/content \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI Tutorial",
    "url": "https://fastapi.tiangolo.com",
    "content_text": "Learn how to build APIs",
    "content_type": "article",
    "category_id": 1,
    "tag_ids": [1, 2]
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "FastAPI Tutorial",
  "url": "https://fastapi.tiangolo.com",
  "content_text": "Learn how to build APIs",
  "content_type": "article",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Tech Articles",
    "description": "Technology articles",
    "user_id": 1,
    "created_at": "2026-01-16T10:00:00"
  },
  "tags": [
    {"id": 1, "name": "python", "created_at": "2026-01-16T10:00:00"},
    {"id": 2, "name": "fastapi", "created_at": "2026-01-16T10:00:00"}
  ],
  "created_at": "2026-01-16T10:00:00",
  "updated_at": null
}
```

### List Content
```bash
curl -X GET "http://localhost:8000/api/v1/content?skip=0&limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Query Parameters:**
- `skip` (optional): Number of items to skip (default: 0)
- `limit` (optional): Max items to return (default: 50, max: 100)

### Search Content
```bash
curl -X GET "http://localhost:8000/api/v1/content/search?q=FastAPI" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Query Parameters:**
- `q` (required): Search query (searches title and content_text)

### Get Single Content
```bash
curl -X GET http://localhost:8000/api/v1/content/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Content
```bash
curl -X PUT http://localhost:8000/api/v1/content/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content_text": "Updated content"
  }'
```

### Delete Content
```bash
curl -X DELETE http://localhost:8000/api/v1/content/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (204):** No content

---

## Tag Endpoints

### Create Tag
```bash
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "python"}'
```

**Note:** Tags are global and case-insensitive. If tag exists, returns existing tag.

### List Tags
```bash
curl -X GET http://localhost:8000/api/v1/tags \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete Tag
```bash
curl -X DELETE http://localhost:8000/api/v1/tags/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Category Endpoints

### Create Category
```bash
curl -X POST http://localhost:8000/api/v1/categories \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Articles",
    "description": "Technology related articles"
  }'
```

### List Categories
```bash
curl -X GET http://localhost:8000/api/v1/categories \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Note:** Returns only categories owned by the authenticated user.

### Get Single Category
```bash
curl -X GET http://localhost:8000/api/v1/categories/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Category
```bash
curl -X PUT http://localhost:8000/api/v1/categories/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "description": "Updated description"
  }'
```

### Delete Category
```bash
curl -X DELETE http://localhost:8000/api/v1/categories/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Testing with Swagger UI

1. Start backend:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. Open browser: http://localhost:8000/docs

3. Test registration:
   - Click on `POST /api/v1/auth/register`
   - Click "Try it out"
   - Fill in the request body
   - Click "Execute"

4. Test login:
   - Click on `POST /api/v1/auth/token`
   - Click "Try it out"
   - Enter username and password
   - Click "Execute"
   - Copy the `access_token` from response

## Automated Testing

Run the test script:
```bash
cd backend
source venv/bin/activate
python test_auth.py
```

## Database

SQLite database file: `backend/app.db`

View users:
```bash
cd backend
sqlite3 app.db "SELECT id, email, username, created_at FROM users;"
```

Clear database (for testing):
```bash
cd backend
rm app.db
# Tables will be recreated on next startup
```

## Security Notes

- Passwords are hashed with bcrypt before storage
- JWT tokens expire after 30 minutes
- Tokens include username in "sub" claim
- SECRET_KEY from environment variables used for signing
- No plaintext passwords are ever stored or logged
