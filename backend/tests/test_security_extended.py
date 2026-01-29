import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_performance_endpoint():
    """Test performance monitoring endpoint"""
    client = TestClient(app)
    
    response = client.get("/api/v1/health/performance")
    
    assert response.status_code == 200
    data = response.json()
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "timestamp" in data
    assert "status" in data
    assert data["status"] == "healthy"

def test_websocket_security_functions():
    """Test WebSocket security functions"""
    from app.core.security import validate_websocket_origin
    from unittest.mock import Mock
    
    # Test valid origin
    mock_websocket = Mock()
    mock_websocket.headers = {"origin": "http://localhost:3000"}
    assert validate_websocket_origin(mock_websocket) == True
    
    # Test invalid origin
    mock_websocket.headers = {"origin": "http://malicious.com"}
    assert validate_websocket_origin(mock_websocket) == False

def test_password_hashing():
    """Test password hashing functions"""
    from app.core.security import get_password_hash, verify_password
    
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) == True
    assert verify_password("wrongpassword", hashed) == False
