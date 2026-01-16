#!/bin/bash

# Phase 2 Testing Quick Start Script

echo "🧪 Phase 2 Content Management Testing"
echo "======================================"
echo ""

# Check if backend is running
echo "1️⃣ Checking backend..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend is NOT running"
    echo "   Start it with: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    echo ""
fi

# Check if frontend is running
echo ""
echo "2️⃣ Checking frontend..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend is NOT running"
    echo "   Start it with: cd frontend && npm run dev"
    echo ""
fi

echo ""
echo "3️⃣ Testing backend API..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
    
    # Check if we can access API docs
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "✅ API docs available at http://localhost:8000/docs"
    fi
else
    echo "❌ Cannot reach backend API"
fi

echo ""
echo "📋 Manual Testing Checklist:"
echo "======================================"
echo ""
echo "1. Open http://localhost:3000"
echo "2. Register a new user or login"
echo "3. Test content creation:"
echo "   - Click 'Add Content'"
echo "   - Fill in title and type"
echo "   - Create some tags"
echo "   - Submit form"
echo ""
echo "4. Test content list:"
echo "   - View all content"
echo "   - Search for content"
echo "   - Click View/Edit/Delete"
echo ""
echo "5. Test content detail:"
echo "   - View full content"
echo "   - Edit content"
echo "   - Delete content"
echo ""
echo "6. Test dashboard:"
echo "   - Check statistics"
echo "   - View recent content"
echo ""
echo "7. Test responsive design:"
echo "   - Open DevTools (F12)"
echo "   - Toggle device toolbar"
echo "   - Test at 320px, 768px, 1920px"
echo ""
echo "📖 Full testing guide: TESTING_GUIDE.md"
echo ""
echo "🚀 Quick backend test:"
echo "   cd backend && python3 test_content_api.py"
echo ""
