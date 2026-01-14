# Setup Instructions

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+

## Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will run at: http://localhost:8000
   API docs at: http://localhost:8000/docs

## Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy environment file:
   ```bash
   cp .env.local.example .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   Frontend will run at: http://localhost:3000

## Verify Setup

1. Backend health check:
   ```bash
   curl http://localhost:8000/health
   ```

2. Open frontend in browser:
   ```
   http://localhost:3000
   ```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── core/            # Configuration
│   │   ├── db/              # Database setup
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── api/routes/      # API endpoints
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
│
└── frontend/
    ├── app/                 # Next.js App Router
    ├── package.json         # Node dependencies
    └── .env.local           # Environment variables
```
