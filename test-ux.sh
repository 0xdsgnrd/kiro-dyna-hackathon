#!/bin/bash

echo "🔧 Testing UX fixes..."

# Start backend
echo "Starting backend..."
cd backend
python -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!

echo "✅ Servers starting..."
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
