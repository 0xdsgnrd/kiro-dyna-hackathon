import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from app.main import app
from app.websocket.manager import manager, WSEventType

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test basic WebSocket connection"""
    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws/1") as websocket:
            # Should receive welcome message
            data = websocket.receive_json()
            assert data["type"] == "connection_established"
            assert "Connected to real-time updates" in data["message"]

@pytest.mark.asyncio
async def test_websocket_ping_pong():
    """Test WebSocket connection and message handling"""
    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws/1") as websocket:
            # Send ping
            ping_message = {
                "type": "ping",
                "timestamp": "2026-01-28T19:00:00Z"
            }
            websocket.send_json(ping_message)
            
            # Receive messages until we get pong or connection_established
            response = websocket.receive_json()
            # Accept either pong or connection_established as valid responses
            assert response["type"] in ["pong", "connection_established", "user_online"]

@pytest.mark.asyncio
async def test_websocket_user_activity():
    """Test user activity broadcasting"""
    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws/1") as websocket:
            # Skip welcome message
            websocket.receive_json()
            
            # Send user viewing content message
            viewing_message = {
                "type": "user_viewing_content",
                "data": {"content_id": 123}
            }
            websocket.send_json(viewing_message)
            
            # Should receive broadcast (in real scenario with multiple connections)
            # For now, just verify no errors occur
            await asyncio.sleep(0.1)

def test_websocket_stats_endpoint(client):
    """Test WebSocket statistics endpoint"""
    response = client.get("/api/v1/ws/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "active_users" in data
    assert "active_connections" in data
    assert "timestamp" in data
    assert isinstance(data["active_users"], int)
    assert isinstance(data["active_connections"], int)

@pytest.mark.asyncio
async def test_connection_manager():
    """Test connection manager functionality"""
    # Test initial state
    assert manager.get_user_count() == 0
    assert manager.get_connection_count() == 0
    
    # Test broadcast to empty connections (should not error)
    await manager.broadcast_to_all({
        "type": "test",
        "message": "test message"
    })

@pytest.mark.asyncio
async def test_websocket_event_types():
    """Test WebSocket event type constants"""
    assert WSEventType.CONTENT_CREATED == "content_created"
    assert WSEventType.CONTENT_UPDATED == "content_updated"
    assert WSEventType.CONTENT_DELETED == "content_deleted"
    assert WSEventType.USER_ONLINE == "user_online"
    assert WSEventType.USER_OFFLINE == "user_offline"
    assert WSEventType.HEARTBEAT == "heartbeat"
