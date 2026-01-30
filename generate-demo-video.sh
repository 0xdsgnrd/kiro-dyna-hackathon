#!/bin/bash

# Content Aggregation Platform - Demo Video Generator
# This script runs Playwright tests to generate demo videos

echo "🎬 Generating Demo Video for Content Aggregation Platform"
echo "======================================================="

cd frontend

# Install Playwright browsers if needed
echo "📦 Installing Playwright browsers..."
npx playwright install

# Run the demo test to generate video
echo "🎥 Running demo test with video recording..."
npx playwright test demo.spec.ts --project=chromium --headed

echo "✅ Demo video generated!"
echo "📁 Videos saved in: frontend/test-results/"
echo "🎬 Look for .webm files in the test results directory"

# List generated videos
echo ""
echo "Generated video files:"
find test-results -name "*.webm" -type f 2>/dev/null || echo "No video files found yet - check test-results directory after test completion"
