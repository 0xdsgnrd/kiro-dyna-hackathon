#!/bin/bash

# Enhanced Log Session Script
# Automatically updates DEVLOG and regenerates Remotion video

PROJECT_ROOT="/Users/kriskutayiah/Desktop/demo-projects/kiro-dyna-hackathon-main"
VIDEO_DIR="$PROJECT_ROOT/devlog-video"
DEVLOG_FILE="$PROJECT_ROOT/DEVLOG.md"

echo "🎬 Starting enhanced log session workflow..."

# Step 1: Parse DEVLOG for session data (this will be done by Kiro)
echo "📖 Reading DEVLOG data..."

# Step 2: Update Remotion component (this will be done by Kiro)
echo "🔄 Updating Remotion video component..."

# Step 3: Regenerate video
echo "🎥 Regenerating video..."
cd "$VIDEO_DIR"
npm run build

# Step 4: Check if video was generated successfully
if [ -f "$VIDEO_DIR/out/devlog.mp4" ]; then
    VIDEO_SIZE=$(ls -lh "$VIDEO_DIR/out/devlog.mp4" | awk '{print $5}')
    echo "✅ Video successfully generated: $VIDEO_SIZE"
else
    echo "❌ Video generation failed"
    exit 1
fi

# Step 5: Return to project root
cd "$PROJECT_ROOT"

echo "🎉 Enhanced log session complete!"
echo "📁 Updated files:"
echo "   - DEVLOG.md"
echo "   - devlog-video/src/Root.tsx"
echo "   - devlog-video/out/devlog.mp4 ($VIDEO_SIZE)"
