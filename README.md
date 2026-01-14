# Content Aggregation SaaS Platform

A modern, full-stack content aggregation platform built with Next.js and FastAPI. This project demonstrates microservices architecture, secure authentication, and modern web development practices.

**Built for**: Kiro CLI Hackathon 2026  
**Status**: MVP - User Management Phase Complete

## 🎯 Project Overview

Content Aggregation Platform allows users to collect, organize, and manage content from multiple sources in one centralized location. The MVP focuses on user authentication and management, with a scalable architecture ready for content aggregation features.

### Key Features

- ✅ **User Authentication**: Secure JWT-based authentication
- ✅ **User Registration & Login**: Complete auth flow with validation
- ✅ **Protected Dashboard**: User-specific dashboard interface
- ✅ **Responsive Design**: Mobile-first UI with Tailwind CSS
- ✅ **Microservices Architecture**: Scalable FastAPI backend
- 🚧 **Content Aggregation**: Coming in Phase 2
- 🚧 **Search & Filtering**: Coming in Phase 2

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
   git clone <your-repo-url>
   cd content-aggregator
   ```

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

### Frontend Tests
```bash
cd frontend
npm test
```

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

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user (protected)

## 🚧 Roadmap

### Phase 1: User Management ✅
- [x] User registration and authentication
- [x] JWT token management
- [x] Protected dashboard
- [x] Responsive UI

### Phase 2: Content Aggregation (Next)
- [ ] Content source integration
- [ ] Content storage and retrieval
- [ ] Tags and categories
- [ ] Search functionality

### Phase 3: Advanced Features
- [ ] Real-time updates
- [ ] Analytics dashboard
- [ ] User preferences
- [ ] Content sharing

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
