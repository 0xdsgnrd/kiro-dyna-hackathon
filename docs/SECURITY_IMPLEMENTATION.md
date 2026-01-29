# Security Enhancement Implementation

## 3.1 Refresh Token Mechanism

### Create backend/app/models/refresh_token.py:
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime, timedelta

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="refresh_tokens")
    
    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self):
        return not self.is_revoked and not self.is_expired
```

### Update backend/app/models/user.py:
```python
# Add to User model
refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
```

### Update backend/app/core/security.py:
```python
import secrets
from datetime import datetime, timedelta

def create_refresh_token(user_id: int, db: Session) -> str:
    """Create a new refresh token for user"""
    from app.models.refresh_token import RefreshToken
    
    # Revoke existing refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    
    # Create new refresh token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=30)
    
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    
    db.add(refresh_token)
    db.commit()
    
    return token

def verify_refresh_token(token: str, db: Session) -> Optional[int]:
    """Verify refresh token and return user_id if valid"""
    from app.models.refresh_token import RefreshToken
    
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()
    
    if not refresh_token or not refresh_token.is_valid:
        return None
    
    return refresh_token.user_id
```

### Update backend/app/api/routes/auth.py:
```python
from app.core.security import create_refresh_token, verify_refresh_token

@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    user_id = verify_refresh_token(refresh_token, db)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Update login endpoint to return refresh token
@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # ... existing login logic ...
    
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(user.id, db)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

## 3.2 Comprehensive Input Validation

### Create backend/app/middleware/validation_middleware.py:
```python
from fastapi import Request, HTTPException, status
from pydantic import ValidationError
import re
from typing import Any, Dict

class ValidationMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Validate request size
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                response = HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Request too large"
                )
                await response(scope, receive, send)
                return
            
            # Validate content type for POST/PUT requests
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.headers.get("content-type", "")
                if not any(ct in content_type for ct in ["application/json", "multipart/form-data", "application/x-www-form-urlencoded"]):
                    response = HTTPException(
                        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        detail="Unsupported media type"
                    )
                    await response(scope, receive, send)
                    return
        
        await self.app(scope, receive, send)

def sanitize_input(data: Any) -> Any:
    """Sanitize input data to prevent XSS and injection attacks"""
    if isinstance(data, str):
        # Remove potentially dangerous characters
        data = re.sub(r'[<>"\']', '', data)
        # Limit string length
        data = data[:1000]
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    
    return data
```

### Create backend/app/schemas/validation.py:
```python
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class ContentCreateValidated(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None
    
    @validator('title', 'content')
    def sanitize_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        # Remove HTML tags
        v = re.sub(r'<[^>]+>', '', v)
        return v.strip()
    
    @validator('url')
    def validate_url(cls, v):
        if v:
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not url_pattern.match(v):
                raise ValueError('Invalid URL format')
        return v

class UserRegistrationValidated(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
```

## 3.3 Enhanced Rate Limiting

### Update backend/app/main.py:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Enhanced rate limiter with user-based limiting
def get_user_id_or_ip(request: Request):
    """Get user ID if authenticated, otherwise use IP"""
    try:
        # Try to get user from token
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        if token:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return f"user:{payload.get('sub', 'anonymous')}"
    except:
        pass
    
    return f"ip:{get_remote_address(request)}"

limiter = Limiter(key_func=get_user_id_or_ip)

# Add different rate limits for different endpoints
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Apply different limits based on endpoint
    path = request.url.path
    
    if path.startswith("/api/v1/auth/"):
        # Stricter limits for auth endpoints
        limiter.limit("5/minute")(lambda: None)()
    elif path.startswith("/api/v1/content"):
        # Moderate limits for content operations
        limiter.limit("100/minute")(lambda: None)()
    else:
        # General API limits
        limiter.limit("200/minute")(lambda: None)()
    
    response = await call_next(request)
    return response
```

### Create backend/app/core/rate_limiting.py:
```python
from functools import wraps
from fastapi import HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
from typing import Dict, List
import asyncio

class AdvancedRateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}
        self.blocked_ips: Dict[str, float] = {}
    
    def is_blocked(self, key: str) -> bool:
        """Check if key is currently blocked"""
        if key in self.blocked_ips:
            if time.time() < self.blocked_ips[key]:
                return True
            else:
                del self.blocked_ips[key]
        return False
    
    def add_request(self, key: str, window: int = 60) -> bool:
        """Add request and check if limit exceeded"""
        now = time.time()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Clean old requests
        self.requests[key] = [req_time for req_time in self.requests[key] if now - req_time < window]
        
        self.requests[key].append(now)
        return len(self.requests[key])
    
    def block_key(self, key: str, duration: int = 300):
        """Block key for specified duration (seconds)"""
        self.blocked_ips[key] = time.time() + duration

advanced_limiter = AdvancedRateLimiter()

def progressive_rate_limit(max_requests: int = 100, window: int = 60, block_duration: int = 300):
    """Progressive rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            key = get_remote_address(request)
            
            if advanced_limiter.is_blocked(key):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="IP temporarily blocked due to excessive requests"
                )
            
            request_count = advanced_limiter.add_request(key, window)
            
            if request_count > max_requests:
                advanced_limiter.block_key(key, block_duration)
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Blocked for {block_duration} seconds."
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
```

## Frontend Security Updates

### Update frontend/lib/api.ts:
```typescript
// Add refresh token handling
let refreshTokenPromise: Promise<string> | null = null;

async function refreshAccessToken(): Promise<string> {
  if (refreshTokenPromise) {
    return refreshTokenPromise;
  }

  refreshTokenPromise = (async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw new Error('Failed to refresh token');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data.access_token;
  })();

  try {
    const token = await refreshTokenPromise;
    return token;
  } finally {
    refreshTokenPromise = null;
  }
}

// Update apiClient to handle token refresh
export const apiClient = {
  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    let token = localStorage.getItem('access_token');
    
    const makeRequest = async (authToken: string | null) => {
      const headers = {
        'Content-Type': 'application/json',
        ...(authToken && { Authorization: `Bearer ${authToken}` }),
        ...options.headers,
      };

      return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    };

    let response = await makeRequest(token);

    // If unauthorized, try to refresh token
    if (response.status === 401 && token) {
      try {
        token = await refreshAccessToken();
        response = await makeRequest(token);
      } catch (error) {
        // Redirect to login if refresh fails
        window.location.href = '/login';
        throw error;
      }
    }

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  },
};
```

## Implementation Commands

```bash
# Phase 3.1 - Refresh Tokens
cd backend
# Create migration for refresh_tokens table
python3 -c "
from app.db.session import engine, Base
from app.models.refresh_token import RefreshToken
Base.metadata.create_all(bind=engine)
"

# Phase 3.2 - Input Validation
# Add validation middleware to main.py
# Update all route handlers to use validated schemas

# Phase 3.3 - Enhanced Rate Limiting
pip install slowapi
# Update main.py with new rate limiting configuration
```

## Success Metrics

- **Refresh Tokens**: Seamless token renewal without user intervention
- **Input Validation**: All inputs sanitized and validated
- **Rate Limiting**: Progressive blocking prevents abuse
- **Security Score**: OWASP compliance improved
