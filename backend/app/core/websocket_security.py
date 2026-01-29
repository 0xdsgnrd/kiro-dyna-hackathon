from fastapi import WebSocket, HTTPException, status
from jose import JWTError, jwt
from app.core.config import settings
from app.models.user import User
from app.db.session import SessionLocal
from typing import Optional

async def get_current_user_websocket(websocket: WebSocket, token: str = None) -> Optional[User]:
    """
    Get current user from WebSocket connection
    For demo purposes, this is simplified. In production, implement proper JWT validation.
    """
    try:
        if not token:
            # For demo, we'll accept user_id from URL path
            # In production, validate JWT token from query params or headers
            return None
        
        # Decode JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        
        if user_id is None:
            return None
            
        # Get user from database
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        finally:
            db.close()
            
    except JWTError:
        return None

def validate_websocket_origin(websocket: WebSocket) -> bool:
    """
    Validate WebSocket origin for security
    """
    origin = websocket.headers.get("origin")
    
    # Allow localhost for development
    allowed_origins = [
        "http://localhost:3000",
        "https://localhost:3000",
        settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else None
    ]
    
    return origin in [o for o in allowed_origins if o is not None]
