#!/bin/bash
# Quick start script for development

echo "🚀 Starting Content Aggregation Platform..."
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "Run: cd backend && python3 -m venv venv && pip install -r requirements.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "Run: cd frontend && npm install"
    exit 1
fi

echo "✅ All dependencies found"
echo ""
echo "📦 Starting Backend (FastAPI)..."
echo "   URL: http://localhost:8000"
echo "   Docs: kiro-cli/docs"
echo ""
echo "📦 Starting Frontend (Next.js)..."
echo "   URL: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
