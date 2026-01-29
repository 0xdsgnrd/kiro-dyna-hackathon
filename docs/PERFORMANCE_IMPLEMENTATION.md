# Performance Optimization Implementation

## 2.1 Database Indexing

### Add to backend/app/models/content.py:
```python
from sqlalchemy import Index

# Add these indexes to the Content model
__table_args__ = (
    Index('idx_content_title', 'title'),
    Index('idx_content_user_id', 'user_id'),
    Index('idx_content_created_at', 'created_at'),
    Index('idx_content_category_id', 'category_id'),
    Index('idx_content_search', 'title', 'content'),  # Composite index for search
)
```

### Create backend/migrations/add_indexes.sql:
```sql
-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_content_title ON content(title);
CREATE INDEX IF NOT EXISTS idx_content_user_id ON content(user_id);
CREATE INDEX IF NOT EXISTS idx_content_created_at ON content(created_at);
CREATE INDEX IF NOT EXISTS idx_content_category_id ON content(category_id);
CREATE INDEX IF NOT EXISTS idx_content_search ON content(title, content);

-- Tag-related indexes
CREATE INDEX IF NOT EXISTS idx_content_tags_content_id ON content_tags(content_id);
CREATE INDEX IF NOT EXISTS idx_content_tags_tag_id ON content_tags(tag_id);
```

## 2.2 Redis Caching Strategy

### Add to backend/requirements.txt:
```
redis>=4.5.0
```

### Create backend/app/core/cache.py:
```python
import redis
import json
from typing import Any, Optional
from app.core.config import settings

# Redis client
redis_client = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=getattr(settings, 'REDIS_DB', 0),
    decode_responses=True
)

class Cache:
    @staticmethod
    def get(key: str) -> Optional[Any]:
        try:
            value = redis_client.get(key)
            return json.loads(value) if value else None
        except:
            return None
    
    @staticmethod
    def set(key: str, value: Any, ttl: int = 300):
        try:
            redis_client.setex(key, ttl, json.dumps(value, default=str))
        except:
            pass
    
    @staticmethod
    def delete(key: str):
        try:
            redis_client.delete(key)
        except:
            pass
    
    @staticmethod
    def clear_pattern(pattern: str):
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except:
            pass

cache = Cache()
```

### Create backend/app/middleware/cache_middleware.py:
```python
from fastapi import Request, Response
from app.core.cache import cache
import hashlib

async def cache_middleware(request: Request, call_next):
    # Only cache GET requests
    if request.method != "GET":
        return await call_next(request)
    
    # Generate cache key
    cache_key = f"api:{hashlib.md5(str(request.url).encode()).hexdigest()}"
    
    # Try to get from cache
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response(
            content=cached_response["content"],
            status_code=cached_response["status_code"],
            headers=cached_response["headers"]
        )
    
    # Process request
    response = await call_next(request)
    
    # Cache successful responses
    if response.status_code == 200:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        cache.set(cache_key, {
            "content": response_body.decode(),
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }, ttl=300)
        
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=response.headers
        )
    
    return response
```

## 2.3 Bundle Optimization

### Update frontend/next.config.js:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enhanced performance optimizations
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['@/components', '@/lib'],
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  
  // Bundle optimization
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      // Split chunks for better caching
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
          common: {
            name: 'common',
            minChunks: 2,
            chunks: 'all',
            enforce: true,
          },
        },
      };
    }
    return config;
  },
  
  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
  },
  
  // Compression and headers
  compress: true,
  poweredByHeader: false,
  
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

### Create frontend/lib/dynamic-imports.ts:
```typescript
import dynamic from 'next/dynamic';
import { LoadingSpinner } from './ui-components';

// Lazy load heavy components
export const DynamicAnalyticsDashboard = dynamic(
  () => import('@/components/AnalyticsDashboard'),
  {
    loading: () => <LoadingSpinner />,
    ssr: false,
  }
);

export const DynamicContentEditor = dynamic(
  () => import('@/components/ContentEditor'),
  {
    loading: () => <LoadingSpinner />,
  }
);

export const DynamicDataVisualization = dynamic(
  () => import('@/components/DataVisualization'),
  {
    loading: () => <LoadingSpinner />,
    ssr: false,
  }
);
```

## Implementation Commands

### Phase 2.1 - Database Indexing:
```bash
# Apply database indexes
cd backend
python3 -c "
from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    with open('migrations/add_indexes.sql', 'r') as f:
        for statement in f.read().split(';'):
            if statement.strip():
                conn.execute(text(statement))
    conn.commit()
"
```

### Phase 2.2 - Redis Setup:
```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Install Python Redis client
cd backend
pip install redis>=4.5.0

# Add cache middleware to main.py
# app.add_middleware(cache_middleware)
```

### Phase 2.3 - Bundle Optimization:
```bash
cd frontend

# Analyze bundle size
npm install --save-dev @next/bundle-analyzer
ANALYZE=true npm run build

# Update imports to use dynamic loading
# Replace heavy component imports with dynamic imports
```

## Success Metrics

- **Database**: Query time reduced by 50%+
- **Caching**: Cache hit ratio > 70%
- **Bundle**: Size reduced by 20%+
- **Performance**: Lighthouse score > 90
