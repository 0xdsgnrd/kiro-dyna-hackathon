# [FEAT-002] Backend User Authentication Service

## Goal
Build a complete FastAPI user authentication service with registration, login, JWT tokens, and password security.

## Description
With the project structure in place, we need to implement the backend authentication service. This includes database models, Pydantic schemas, security utilities, and API endpoints for user registration and login.

---

## Requirements

- **User Model**: SQLAlchemy model with email, username, hashed password, timestamps
- **Pydantic Schemas**: Request/response schemas for user data and tokens
- **Security Utilities**: Password hashing (bcrypt) and JWT token generation
- **Registration Endpoint**: `POST /api/v1/auth/register` creates new users
- **Login Endpoint**: `POST /api/v1/auth/token` returns JWT token
- **Password Validation**: Passwords hashed before storage, never stored plaintext

### Non-Goals
- User profile endpoints (GET/PUT/DELETE)
- Password reset functionality
- Email verification
- Token refresh mechanism

---

## Acceptance Criteria

- [ ] User model created with proper fields and indexes
- [ ] Database tables created automatically on startup
- [ ] Registration endpoint accepts email, username, password and returns user data
- [ ] Registration endpoint rejects duplicate email/username with 400 error
- [ ] Login endpoint accepts username/password and returns JWT token
- [ ] Login endpoint rejects invalid credentials with 401 error
- [ ] Passwords hashed with bcrypt (verify hash never matches plaintext)
- [ ] JWT tokens include username in payload and expire after 30 minutes
- [ ] All endpoints documented in Swagger UI at `/docs`
- [ ] Backend tests pass with 80%+ coverage

---

## Technical Context

- SQLAlchemy models in `backend/app/models/user.py`
- Pydantic schemas in `backend/app/schemas/user.py`
- Security utilities in `backend/app/core/security.py`
- Auth routes in `backend/app/api/routes/auth.py`
- Use FastAPI dependency injection for database sessions
- JWT tokens use HS256 algorithm with SECRET_KEY from environment

---

## Risks / Open Questions

- **Token Expiration**: 30 minutes may be too short for user experience
- **Username vs Email Login**: Currently using username, consider email login

---

## Dependencies

- FEAT-001 (Project Setup) must be complete

---

## Success Metrics

- 80%+ test coverage for auth endpoints
- API response time < 200ms
- Zero plaintext passwords in database

---

## Definition of Done

- All acceptance criteria met
- Backend validation passes: `black`, `flake8`, `mypy`, `pytest`
- Manual testing via Swagger UI successful
- API endpoints documented
