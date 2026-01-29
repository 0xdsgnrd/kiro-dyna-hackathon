from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.websocket.manager import manager, WSEventType, broadcast_user_activity
from app.core.security import get_current_user_websocket
from app.models.user import User
import json
import asyncio

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Main WebSocket endpoint for real-time communication"""
    
    # Authenticate user (simplified for demo)
    # In production, use proper JWT validation
    try:
        await manager.connect(websocket, user_id)
        
        # Notify other users that this user is online
        await broadcast_user_activity(user_id, WSEventType.USER_ONLINE)
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await handle_websocket_message(websocket, user_id, message)
                
        except WebSocketDisconnect:
            pass
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)
        # Notify other users that this user is offline
        await broadcast_user_activity(user_id, WSEventType.USER_OFFLINE)

async def handle_websocket_message(websocket: WebSocket, user_id: int, message: dict):
    """Handle incoming WebSocket messages"""
    
    message_type = message.get("type")
    data = message.get("data", {})
    
    if message_type == "ping":
        # Respond to ping with pong
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }, websocket)
    
    elif message_type == "user_viewing_content":
        # Broadcast that user is viewing specific content
        content_id = data.get("content_id")
        if content_id:
            await broadcast_user_activity(user_id, WSEventType.USER_VIEWING_CONTENT, {
                "content_id": content_id
            })
    
    elif message_type == "user_editing_content":
        # Broadcast that user is editing specific content
        content_id = data.get("content_id")
        if content_id:
            await broadcast_user_activity(user_id, WSEventType.USER_EDITING_CONTENT, {
                "content_id": content_id,
                "field": data.get("field"),
                "cursor_position": data.get("cursor_position")
            })
    
    elif message_type == "typing_indicator":
        # Broadcast typing indicator for collaborative editing
        await manager.broadcast_to_all({
            "type": "typing_indicator",
            "user_id": user_id,
            "content_id": data.get("content_id"),
            "is_typing": data.get("is_typing", False)
        })

@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "active_users": manager.get_user_count(),
        "active_connections": manager.get_connection_count(),
        "timestamp": asyncio.get_event_loop().time()
    }
