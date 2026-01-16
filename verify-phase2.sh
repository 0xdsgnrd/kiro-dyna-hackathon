#!/bin/bash

# Phase 2 Verification Script
# Tests all Phase 2 features

echo "🧪 Phase 2 Feature Verification"
echo "================================"
echo ""

# Backend Tests
echo "📦 Running Backend Tests..."
cd backend
source venv/bin/activate
PYTHONPATH=$(pwd) pytest tests/ -v --cov=app --tb=short 2>&1 | tail -20
BACKEND_EXIT=$?
cd ..

echo ""
echo "================================"
echo ""

# Frontend Tests
echo "🎨 Running Frontend Tests..."
cd frontend
npm test 2>&1 | tail -15
FRONTEND_EXIT=$?
cd ..

echo ""
echo "================================"
echo ""

# Frontend Build
echo "🏗️  Building Frontend..."
cd frontend
npm run build 2>&1 | tail -10
BUILD_EXIT=$?
cd ..

echo ""
echo "================================"
echo ""

# Summary
echo "📊 Test Summary"
echo "================================"

if [ $BACKEND_EXIT -eq 0 ]; then
    echo "✅ Backend Tests: PASSED"
else
    echo "❌ Backend Tests: FAILED"
fi

if [ $FRONTEND_EXIT -eq 0 ]; then
    echo "✅ Frontend Tests: PASSED"
else
    echo "❌ Frontend Tests: FAILED"
fi

if [ $BUILD_EXIT -eq 0 ]; then
    echo "✅ Production Build: SUCCESS"
else
    echo "❌ Production Build: FAILED"
fi

echo ""

if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ] && [ $BUILD_EXIT -eq 0 ]; then
    echo "🎉 Phase 2 Complete - All Tests Passing!"
    exit 0
else
    echo "⚠️  Some tests failed. Please review above."
    exit 1
fi
