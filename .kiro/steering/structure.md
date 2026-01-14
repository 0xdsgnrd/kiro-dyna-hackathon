# Project Structure

## Directory Layout

```
content-aggregator/
├── frontend/                 # Next.js application
│   ├── app/                 # App Router pages
│   │   ├── page.tsx        # Landing page
│   │   ├── login/          # Login page
│   │   ├── register/       # Registration page
│   │   ├── dashboard/      # User dashboard
│   │   └── layout.tsx      # Root layout
│   ├── components/          # Reusable React components
│   ├── contexts/            # React contexts (Auth, etc.)
│   ├── lib/                 # Utilities and API client
│   ├── public/              # Static assets
│   └── __tests__/           # Frontend tests
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Route handlers
│   │   ├── core/           # Core utilities (config, security)
│   │   └── db/             # Database configuration
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
├── .kiro/                  # Kiro CLI configuration
│   ├── steering/           # Project documentation
│   └── prompts/            # Custom prompts
│
├── DEVLOG.md              # Development log
└── README.md              # Project documentation
```

## File Naming Conventions

### Frontend (Next.js)
- **Pages**: `page.tsx` (App Router convention)
- **Components**: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- **Utilities**: `camelCase.ts` (e.g., `apiClient.ts`)
- **Contexts**: `PascalCase.tsx` with `Context` suffix (e.g., `AuthContext.tsx`)

### Backend (FastAPI)
- **Modules**: `snake_case.py` (e.g., `user_service.py`)
- **Models**: `snake_case.py` (e.g., `user.py`)
- **Routes**: `snake_case.py` (e.g., `auth.py`)

## Module Organization

### Frontend
- **app/**: Next.js App Router pages and layouts
- **components/**: Shared UI components (buttons, forms, cards)
- **contexts/**: React Context providers for global state
- **lib/**: Utility functions, API client, helpers

### Backend
- **models/**: Database models (SQLAlchemy)
- **schemas/**: Request/response schemas (Pydantic)
- **api/routes/**: API endpoint handlers
- **core/**: Configuration, security, shared utilities
- **db/**: Database connection and session management

## Configuration Files

### Frontend
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `tailwind.config.ts` - Tailwind CSS configuration
- `next.config.js` - Next.js configuration
- `.env.local` - Environment variables (not committed)

### Backend
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not committed)
- `pyproject.toml` - Python project metadata (optional)

## Documentation Structure

- `README.md` - Project overview, setup, and usage
- `DEVLOG.md` - Development timeline and decisions
- `.kiro/steering/` - Project steering documents
  - `product.md` - Product overview
  - `tech.md` - Technical architecture
  - `structure.md` - This file

## Asset Organization

### Frontend Assets
- `public/` - Static files (images, fonts, icons)
- `app/globals.css` - Global styles and Tailwind imports

### Backend Assets
- No static assets (API only)

## Build Artifacts

### Frontend
- `.next/` - Next.js build output (gitignored)
- `out/` - Static export output (gitignored)
- `node_modules/` - Dependencies (gitignored)

### Backend
- `__pycache__/` - Python bytecode (gitignored)
- `venv/` or `env/` - Virtual environment (gitignored)
- `*.pyc` - Compiled Python files (gitignored)
- `app.db` - SQLite database (gitignored in dev)

## Environment-Specific Files

### Development
- Frontend: `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
- Backend: `.env` with `DATABASE_URL=sqlite:///./app.db`

### Production
- Frontend: Environment variables set in deployment platform
- Backend: Environment variables with PostgreSQL connection string
- Use strong `SECRET_KEY` for JWT signing
