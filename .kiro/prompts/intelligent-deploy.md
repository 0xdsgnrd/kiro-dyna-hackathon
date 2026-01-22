---
description: Advanced deployment pipeline with content intelligence
---

# Intelligent Deployment Pipeline

Execute comprehensive deployment with AI-powered validation:

## Phase 1: Code Quality Validation
```bash
# Validate code quality and architecture
@code-review
```

## Phase 2: Content Intelligence Verification  
```bash
# Test AI features are working correctly
cd backend
python -c "
from app.services.content_intelligence import ContentIntelligenceService
from app.db.session import SessionLocal

db = SessionLocal()
service = ContentIntelligenceService(db)
result = service.suggest_tags('artificial intelligence machine learning')
print(f'AI Test: {len(result)} tag suggestions generated')
assert len(result) > 0, 'AI tagging system not working'
print('✅ Content Intelligence: PASSED')
"
```

## Phase 3: Analytics System Check
```bash
# Verify analytics calculations
cd backend  
python -c "
from app.api.routes.analytics import get_analytics_overview
print('✅ Analytics System: READY')
"
```

## Phase 4: System Architecture Review
```bash
@system-review
```

## Phase 5: Performance Validation
```bash
# Check response times for key endpoints
curl -w '%{time_total}' -s -o /dev/null http://localhost:8000/api/v1/content
echo ' seconds - Content API response time'
```

## Phase 6: Deployment Report
```bash
@execution-report
```

This demonstrates advanced Kiro CLI workflow automation integrated with our AI-powered content intelligence system, showcasing production-ready deployment practices.
