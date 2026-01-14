# Authentication API Quick Reference

## Endpoints

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
