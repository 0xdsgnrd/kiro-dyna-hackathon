#!/bin/bash
# Comprehensive Test Data Creation for Hackathon Demo

echo "🎯 Creating comprehensive test data for hackathon demo..."

# Get authentication token
echo "🔐 Getting authentication token..."
TOKEN=$(curl -s http://localhost:8000/api/v1/auth/token -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=demo&password=demo123" | jq -r '.access_token')

if [ "$TOKEN" = "null" ]; then
    echo "❌ Failed to get token. Make sure demo user exists and servers are running."
    exit 1
fi

echo "✅ Token obtained"

# Create Categories
echo "📁 Creating categories..."
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

curl -s -X POST "http://localhost:8000/api/v1/categories" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Research", "description": "Research papers and studies"}' > /dev/null

# Create Tags
echo "🏷️  Creating tags..."
TAGS=("javascript" "react" "nextjs" "python" "fastapi" "tutorial" "productivity" "ai" "machine-learning" "web-development" "mobile" "ios" "android" "startup" "marketing" "design-systems" "ux" "ui" "figma" "typescript")

for tag in "${TAGS[@]}"; do
    curl -s -X POST "http://localhost:8000/api/v1/tags" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"name\": \"$tag\"}" > /dev/null
done

# Create Content Sources
echo "📡 Creating content sources..."
curl -s -X POST "http://localhost:8000/api/v1/sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "source_type": "rss", "description": "Latest tech news and startup coverage"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hacker News", "url": "https://news.ycombinator.com/", "source_type": "webpage", "description": "Tech community discussions"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Dev.to", "url": "https://dev.to/feed", "source_type": "rss", "description": "Developer community articles"}' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Medium Design", "url": "https://medium.com/topic/design/feed", "source_type": "rss", "description": "Design articles and insights"}' > /dev/null

# Create Content Items
echo "📝 Creating content items..."

# Technology Articles
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Building Modern Web Apps with Next.js 14",
    "content_text": "A comprehensive guide to building production-ready web applications using Next.js 14 with the new App Router, Server Components, and advanced optimization techniques.",
    "content_type": "article",
    "url": "https://example.com/nextjs-guide",
    "category_id": 1,
    "tag_ids": [1, 2, 3]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI vs Django: Performance Comparison 2026",
    "content_text": "An in-depth analysis comparing FastAPI and Django performance, developer experience, and ecosystem maturity for modern Python web development.",
    "content_type": "article",
    "url": "https://example.com/fastapi-django",
    "category_id": 1,
    "tag_ids": [4, 5, 6]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "TypeScript Best Practices for Large Applications",
    "content_text": "Essential TypeScript patterns, configurations, and architectural decisions for scaling applications with type safety and maintainability.",
    "content_type": "article",
    "url": "https://example.com/typescript-best-practices",
    "category_id": 1,
    "tag_ids": [1, 20, 6]
  }' > /dev/null

# Business Articles
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "SaaS Metrics That Actually Matter in 2026",
    "content_text": "Beyond vanity metrics: the key performance indicators that successful SaaS companies track to drive sustainable growth and customer satisfaction.",
    "content_type": "article",
    "url": "https://example.com/saas-metrics",
    "category_id": 2,
    "tag_ids": [14, 15]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Remote Team Management: Lessons from 100+ Startups",
    "content_text": "Practical strategies for building and managing high-performing remote teams, based on interviews with successful startup founders and CTOs.",
    "content_type": "article",
    "url": "https://example.com/remote-management",
    "category_id": 2,
    "tag_ids": [7, 14]
  }' > /dev/null

# Design Articles
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design Systems at Scale: Component Architecture",
    "content_text": "How to build and maintain design systems that scale across multiple products and teams, with real examples from Airbnb, Shopify, and Atlassian.",
    "content_type": "article",
    "url": "https://example.com/design-systems-scale",
    "category_id": 3,
    "tag_ids": [16, 17, 18, 19]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "UX Research Methods for Product Teams",
    "content_text": "A practical guide to user research methodologies, from user interviews to usability testing, with templates and real-world case studies.",
    "content_type": "article",
    "url": "https://example.com/ux-research-methods",
    "category_id": 3,
    "tag_ids": [17, 18]
  }' > /dev/null

# Video Content
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI in Web Development: 2026 Trends",
    "content_text": "A 45-minute deep dive into how AI is transforming web development, from code generation to automated testing and deployment optimization.",
    "content_type": "video",
    "url": "https://youtube.com/watch?v=example1",
    "category_id": 1,
    "tag_ids": [8, 9, 10]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mobile App Development with React Native",
    "content_text": "Complete tutorial series covering React Native development from setup to App Store deployment, including navigation, state management, and native modules.",
    "content_type": "video",
    "url": "https://youtube.com/watch?v=example2",
    "category_id": 1,
    "tag_ids": [2, 11, 12, 13]
  }' > /dev/null

# Personal Notes
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly Reflection: Q1 2026 Goals",
    "content_text": "Personal reflection on Q1 progress, key learnings from building the content aggregation platform, and adjustments for Q2 objectives.",
    "content_type": "note",
    "category_id": 4,
    "tag_ids": [7]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Productivity System: Time Blocking Method",
    "content_text": "My personal implementation of time blocking for deep work sessions, including tools, templates, and lessons learned after 6 months of consistent use.",
    "content_type": "note",
    "category_id": 4,
    "tag_ids": [7]
  }' > /dev/null

# Links
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Awesome Developer Tools 2026",
    "content_text": "Curated list of essential developer tools, VS Code extensions, CLI utilities, and productivity apps that every developer should know about.",
    "content_type": "link",
    "url": "https://github.com/awesome-dev-tools-2026",
    "category_id": 1,
    "tag_ids": [7, 10]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Startup Funding Database",
    "content_text": "Comprehensive database of startup funding rounds, investor contacts, and application templates for seed to Series A funding.",
    "content_type": "link",
    "url": "https://example.com/funding-database",
    "category_id": 2,
    "tag_ids": [14]
  }' > /dev/null

# Research Content
curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Large Language Models in Software Development",
    "content_text": "Academic paper analyzing the impact of LLMs on developer productivity, code quality, and software engineering practices across 500+ development teams.",
    "content_type": "article",
    "url": "https://arxiv.org/example-paper",
    "category_id": 5,
    "tag_ids": [8, 9]
  }' > /dev/null

curl -s -X POST "http://localhost:8000/api/v1/content" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "User Interface Design Patterns Study",
    "content_text": "Research study examining the effectiveness of different UI patterns across mobile and web applications, with data from 10,000+ user interactions.",
    "content_type": "article",
    "url": "https://example.com/ui-patterns-study",
    "category_id": 5,
    "tag_ids": [17, 18]
  }' > /dev/null

echo "✅ Test data creation complete!"
echo ""
echo "📊 Created:"
echo "  • 5 Categories (Technology, Business, Design, Personal, Research)"
echo "  • 20 Tags (javascript, react, nextjs, python, etc.)"
echo "  • 4 Content Sources (TechCrunch, Hacker News, Dev.to, Medium Design)"
echo "  • 15 Content Items (articles, videos, notes, links)"
echo ""
echo "🎯 Your app now has comprehensive test data for the hackathon demo!"
echo "🌐 Visit http://localhost:3000 to see the populated app"
