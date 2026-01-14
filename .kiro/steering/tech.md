# Technical Architecture

## Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **State Management**: React Context API
- **HTTP Client**: Fetch API
- **Build Tool**: Next.js built-in (Turbopack)

### Backend
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **Validation**: Pydantic 2+
- **ORM**: SQLAlchemy
- **Database**: SQLite (dev), PostgreSQL (production)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

### Development Tools
- **Version Control**: Git
- **Package Managers**: npm (frontend), pip (backend)
- **Code Quality**: ESLint, Prettier (frontend), Black, Flake8 (backend)
- **Type Checking**: TypeScript (frontend), mypy (backend)

## Architecture Overview

**Microservices Architecture:**
```
Frontend (Next.js) → API Gateway → User Service (FastAPI) → Database
                                 → Content Service (Future)
                                 → Analytics Service (Future)
```

**Current Phase**: User Management Service
**Future Services**: Content aggregation, search, analytics

## Development Environment

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### Setup Instructions
1. Clone repository
2. Backend: Create venv, install requirements
3. Frontend: npm install
4. Configure environment variables
5. Run backend: `uvicorn app.main:app --reload`
6. Run frontend: `npm run dev`

## Code Standards

### TypeScript/React
- Use functional components with hooks
- Prefer TypeScript strict mode
- Use Tailwind utility classes (no custom CSS unless necessary)
- Client components marked with 'use client'
- Server components by default

### Python/FastAPI
- Follow PEP 8 style guide
- Use type hints for all functions
- Pydantic models for validation
- Async/await for I/O operations
- Dependency injection pattern

### Naming Conventions
- **Frontend**: camelCase for variables, PascalCase for components
- **Backend**: snake_case for variables/functions, PascalCase for classes
- **Files**: kebab-case for frontend, snake_case for backend

## Testing Strategy

### Backend Testing
- **Framework**: pytest + pytest-asyncio
- **Coverage**: 80%+ for services
- **Types**: Unit tests, integration tests
- **Location**: `backend/tests/`

### Frontend Testing
- **Framework**: Jest + React Testing Library
- **Coverage**: 70%+ for critical paths
- **Types**: Component tests, integration tests
- **Location**: `frontend/__tests__/`

## Deployment Process

### Development
- Backend: `uvicorn app.main:app --reload` (port 8000)
- Frontend: `npm run dev` (port 3000)

### Production (Future)
- Backend: Docker container → AWS ECS/Lambda
- Frontend: `npm run build` → Vercel/Netlify
- Database: AWS RDS (PostgreSQL)

## Performance Requirements

- Page load time: < 2 seconds
- API response time: < 200ms (p95)
- Support 100+ concurrent users (MVP)
- Mobile-responsive (320px+)

## Security Considerations

### Authentication
- JWT tokens with 30-minute expiration
- Secure password hashing (bcrypt)
- Token stored in localStorage (consider httpOnly cookies for production)

### API Security
- CORS restricted to frontend origin
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- Rate limiting (future)

### Data Protection
- HTTPS in production
- Environment variables for secrets
- No sensitive data in logs
- Regular dependency updates
