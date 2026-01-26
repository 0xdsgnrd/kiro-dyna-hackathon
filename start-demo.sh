#!/bin/bash
# Hackathon Demo Setup Script

echo "🚀 Starting Content Aggregation Platform Demo..."

# Start backend
echo "📡 Starting backend server..."
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend  
echo "🌐 Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for servers to start
sleep 5

# Create demo user
echo "👤 Creating demo user..."
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "email": "demo@example.com", "password": "demo123"}' \
  > /dev/null 2>&1

# Get token for demo user
TOKEN=$(curl -s http://localhost:8000/api/v1/auth/token -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=demo&password=demo123" | jq -r '.access_token')

# Create default categories
echo "📁 Creating default categories..."
curl -s -X POST "http://localhost:8000/api/v1/categories" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Technology", "description": "Tech articles and resources"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/categories" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Business", "description": "Business and entrepreneurship"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/categories" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Design", "description": "Design and UX resources"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/categories" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Personal", "description": "Personal notes and thoughts"}' > /dev/null

# Create default tags
echo "🏷️  Creating default tags..."
curl -s -X POST "http://localhost:8000/api/v1/tags" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "javascript"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/tags" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "react"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/tags" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "tutorial"}' > /dev/null

# Create comprehensive test data
echo "🎯 Creating comprehensive test data..."
./create-test-data.sh > /dev/null 2>&1

echo "✅ Demo ready!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend API: http://localhost:8000/docs"
echo "👤 Demo Login: demo / demo123"
echo ""
echo "Press Ctrl+C to stop servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
