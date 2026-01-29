from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime
from app.core.security import get_current_user_websocket
from app.models.user import User

class ConnectionManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Store connection metadata
        self.connection_metadata: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow(),
            "last_ping": datetime.utcnow()
        }
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "message": "Connected to real-time updates",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        metadata = self.connection_metadata.get(websocket)
        if metadata:
            user_id = metadata["user_id"]
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            del self.connection_metadata[websocket]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except:
            self.disconnect(websocket)
    
    async def send_to_user(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            disconnected = []
            for websocket in self.active_connections[user_id].copy():
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)
            
            # Clean up disconnected websockets
            for websocket in disconnected:
                self.disconnect(websocket)
    
    async def broadcast_to_all(self, message: dict):
        disconnected = []
        for user_connections in self.active_connections.values():
            for websocket in user_connections.copy():
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket)
    
    def get_user_count(self) -> int:
        return len(self.active_connections)
    
    def get_connection_count(self) -> int:
        return sum(len(connections) for connections in self.active_connections.values())

# Global connection manager instance
manager = ConnectionManager()

# WebSocket event types
class WSEventType:
    # Content events
    CONTENT_CREATED = "content_created"
    CONTENT_UPDATED = "content_updated"
    CONTENT_DELETED = "content_deleted"
    
    # User activity
    USER_ONLINE = "user_online"
    USER_OFFLINE = "user_offline"
    
    # System events
    SYSTEM_NOTIFICATION = "system_notification"
    HEARTBEAT = "heartbeat"
    
    # Collaboration events
    USER_VIEWING_CONTENT = "user_viewing_content"
    USER_EDITING_CONTENT = "user_editing_content"

async def broadcast_content_event(event_type: str, content_data: dict, user_id: int = None):
    """Broadcast content-related events to relevant users"""
    message = {
        "type": event_type,
        "data": content_data,
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id
    }
    
    if user_id:
        # Send to specific user
        await manager.send_to_user(message, user_id)
    else:
        # Broadcast to all users
        await manager.broadcast_to_all(message)

async def broadcast_user_activity(user_id: int, activity_type: str, data: dict = None):
    """Broadcast user activity to other users"""
    message = {
        "type": activity_type,
        "user_id": user_id,
        "data": data or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    
    await manager.broadcast_to_all(message)

# Heartbeat task to keep connections alive
async def heartbeat_task():
    while True:
        await asyncio.sleep(30)  # Send heartbeat every 30 seconds
        await manager.broadcast_to_all({
            "type": WSEventType.HEARTBEAT,
            "timestamp": datetime.utcnow().isoformat(),
            "active_users": manager.get_user_count(),
            "active_connections": manager.get_connection_count()
        })
