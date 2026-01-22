#!/bin/bash

echo "🚀 Testing Content Aggregation Platform"
echo "========================================"

# Test Backend
echo "📡 Testing Backend (http://localhost:8000)..."
HEALTH=$(curl -s http://localhost:8000/health)
if [[ $HEALTH == *"healthy"* ]]; then
    echo "✅ Backend health check: PASSED"
else
    echo "❌ Backend health check: FAILED"
    exit 1
fi

# Test API Documentation
DOC_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [[ $DOC_STATUS == "200" ]]; then
    echo "✅ API documentation: ACCESSIBLE"
else
    echo "❌ API documentation: FAILED"
fi

# Test Frontend
echo "🌐 Testing Frontend (http://localhost:3000)..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [[ $FRONTEND_STATUS == "200" ]]; then
    echo "✅ Frontend: ACCESSIBLE"
else
    echo "❌ Frontend: FAILED"
    exit 1
fi

# Test API Endpoints
echo "🔐 Testing Authentication API..."

# Test Registration
REG_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","email":"test2@example.com","password":"testpass123"}')

if [[ $REG_RESPONSE == *"testuser2"* ]]; then
    echo "✅ User registration: PASSED"
else
    echo "❌ User registration: FAILED"
fi

# Test Login
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser2&password=testpass123")

if [[ $LOGIN_RESPONSE == *"access_token"* ]]; then
    echo "✅ User login: PASSED"
else
    echo "❌ User login: FAILED"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📋 Server Status:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 To stop servers:"
echo "   pkill -f uvicorn"
echo "   pkill -f next"
