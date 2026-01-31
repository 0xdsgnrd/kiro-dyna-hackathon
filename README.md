# Content Aggregation SaaS Platform

A modern, full-stack content aggregation platform built with Next.js and FastAPI. This project demonstrates microservices architecture, secure authentication, and modern web development practices.

**Built for**: Kiro CLI Hackathon 2026  
**Status**: Phase 5 Complete - Full Mobile & PWA Platform

## 🎯 Project Overview

Content Aggregation Platform allows users to collect, organize, and manage content from multiple sources in one centralized location. The platform features complete user authentication, content management with tags and categories, and advanced search and filtering capabilities.

### Key Features

- ✅ **User Authentication**: Secure JWT-based authentication
- ✅ **User Registration & Login**: Complete auth flow with validation
- ✅ **Protected Dashboard**: User-specific dashboard with statistics
- ✅ **Content Management**: Full CRUD operations for content items
- ✅ **Tags & Categories**: Organize content with tags and categories
- ✅ **Advanced Search**: Search by title, content, tags with filters
- ✅ **Filtering & Sorting**: Filter by category, type, tag; sort by date or title
- ✅ **Responsive Design**: Mobile-first UI with Tailwind CSS
- ✅ **Microservices Architecture**: Scalable FastAPI backend
- ✅ **Comprehensive Testing**: 87% backend, 80%+ frontend coverage
- ✅ **Real-time Features**: WebSocket integration with live updates
- ✅ **Production Deployment**: Complete AWS infrastructure with CI/CD
- ✅ **PWA Implementation**: Offline support, install prompts, push notifications
- ✅ **Mobile Optimization**: Touch gestures, haptic feedback, voice search

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      Next.js Frontend (Port 3000)   │
│   TypeScript + Tailwind CSS         │
│   - Landing Page                    │
│   - Auth Pages (Login/Register)     │
│   - User Dashboard                  │
└──────────────┬──────────────────────┘
               │ REST API
               ▼
┌─────────────────────────────────────┐
│   FastAPI Backend (Port 8000)       │
│   Python + Pydantic                 │
│   - User Management                 │
│   - JWT Authentication              │
│   - API Endpoints                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Database (SQLite/PostgreSQL)   │
│   - User Data                       │
│   - Session Management              │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone --recursive <your-repo-url>
   cd content-aggregator
   ```
   > **Note:** The `--recursive` flag is required because the frontend is a git submodule. If you already cloned without it, run: `git submodule update --init`

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure backend environment**
   ```bash
   # Create .env file in backend/
   echo "SECRET_KEY=your-secret-key-change-in-production" > .env
   echo "DATABASE_URL=sqlite:///./app.db" >> .env
   ```

4. **Start the backend**
   ```bash
   uvicorn app.main:app --reload
   # Backend runs at http://localhost:8000
   # API docs at http://localhost:8000/docs
   ```

5. **Set up the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   ```

6. **Configure frontend environment**
   ```bash
   # Create .env.local file in frontend/
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   ```

7. **Start the frontend**
   ```bash
   npm run dev
   # Frontend runs at http://localhost:3000
   ```

### First Use

1. Navigate to `http://localhost:3000`
2. Click "Get Started" or "Sign In"
3. Register a new account
4. Login and access your dashboard

## 📁 Project Structure

```
content-aggregator/
├── frontend/                 # Next.js application
│   ├── app/                 # App Router pages
│   │   ├── page.tsx        # Landing page
│   │   ├── login/          # Login page
│   │   ├── register/       # Registration page
│   │   └── dashboard/      # User dashboard
│   ├── contexts/            # React contexts (Auth)
│   ├── lib/                 # API client and utilities
│   └── __tests__/           # Frontend tests
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI entry point
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Config and security
│   │   └── db/             # Database setup
│   └── tests/              # Backend tests
│
├── .kiro/                  # Kiro CLI configuration
├── DEVLOG.md              # Development log
└── README.md              # This file
```

## 🛠️ Technology Stack

### Frontend
- **Next.js 14+** - React framework with App Router
- **TypeScript 5+** - Type-safe JavaScript
- **Tailwind CSS 3+** - Utility-first CSS framework
- **React Context API** - State management

### Backend
- **FastAPI 0.109+** - Modern Python web framework
- **Pydantic 2+** - Data validation
- **SQLAlchemy** - ORM for database operations
- **python-jose** - JWT token handling
- **passlib** - Password hashing with bcrypt

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production database (recommended)

## 🔐 Security

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with salt
- **CORS Protection**: Restricted to frontend origin
- **Input Validation**: Pydantic schemas for all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

**Coverage**: 87% (29 tests passing)
- Authentication tests
- Content CRUD tests
- User isolation tests
- Search and filtering tests
- Tag and category tests

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage  # With coverage report
```

**Coverage**: 80%+ for critical paths (17 tests passing)
- API client tests
- Authentication flow tests
- Content management tests

### Code Quality
```bash
# Backend
cd backend
black app/
flake8 app/
mypy app/

# Frontend
cd frontend
npm run lint
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

**Coverage**: 95% (10/10 tests passing)

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage  # With coverage report
```

**Coverage**: 79.6% for critical paths (4/4 tests passing)

### Code Quality

**Backend:**
```bash
cd backend
# Type checking (requires mypy)
python3 -m pip install mypy
python3 -m mypy app/

# Code formatting (requires black)
python3 -m pip install black
python3 -m black app/

# Linting (requires flake8)
python3 -m pip install flake8
python3 -m flake8 app/
```

**Frontend:**
```bash
cd frontend
# Linting
npm run lint

# Type checking
npx tsc --noEmit
```

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

**Authentication:**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user (protected)

**Content Management:**
- `POST /api/v1/content` - Create content
- `GET /api/v1/content` - List all content (paginated)
- `GET /api/v1/content/search` - Search and filter content
- `GET /api/v1/content/{id}` - Get single content item
- `PUT /api/v1/content/{id}` - Update content
- `DELETE /api/v1/content/{id}` - Delete content

**Tags & Categories:**
- `GET /api/v1/tags` - List all tags
- `POST /api/v1/tags` - Create tag
- `GET /api/v1/categories` - List all categories
- `POST /api/v1/categories` - Create category

## 🚧 Roadmap

### Phase 1: User Management ✅
- [x] User registration and authentication
- [x] JWT token management
- [x] Protected dashboard
- [x] Responsive UI

### Phase 2: Content Management ✅
- [x] Content CRUD operations
- [x] Tags and categories
- [x] Search and filtering
- [x] Advanced sorting
- [x] Comprehensive testing

### Phase 3: Advanced Features (Planned)
- [ ] External content source integration (RSS, APIs)
- [ ] Analytics dashboard with usage insights
- [ ] AI-powered content intelligence (auto-tagging, recommendations)
- [ ] User preferences and theme customization
- [ ] Content sharing and collaboration
- [ ] Export/import system with data portability

## 🤝 Development Workflow

This project uses Kiro CLI for development automation:

```bash
# Load project context
@prime

# Plan new features
@plan-feature "feature description"

# Execute implementation plans
@execute .agents/plans/plan-file.md

# Review code quality
@code-review

# Update development log
@log-session
```

See [DEVLOG.md](DEVLOG.md) for detailed development history.

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Activate virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check `.env` file exists with required variables

### Frontend won't start
- Ensure Node.js 18+ is installed
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check `.env.local` file exists with `NEXT_PUBLIC_API_URL`

### CORS errors
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/app/main.py`
- Verify frontend URL matches CORS allowed origins

### Authentication not working
- Check JWT token in browser localStorage
- Verify backend SECRET_KEY is set
- Check token expiration (default 30 minutes)

## 📄 License

MIT License - See LICENSE file for details

## 🏆 Hackathon Submission

This project was built for the Kiro CLI Hackathon 2026. Key highlights:

- **Kiro CLI Integration**: Extensive use of custom prompts and workflow automation
- **Clean Architecture**: Microservices-ready design
- **Modern Stack**: Latest versions of Next.js and FastAPI
- **Documentation**: Comprehensive README and DEVLOG
- **Best Practices**: Type safety, testing, security

For detailed development process, see [DEVLOG.md](DEVLOG.md).

---

**Built with ❤️ using Kiro CLI**
