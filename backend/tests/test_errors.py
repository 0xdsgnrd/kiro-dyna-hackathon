import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_404_endpoints():
    """Test non-existent endpoints return 404"""
    client = TestClient(app)
    
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404

def test_unauthorized_access():
    """Test protected endpoints without auth return 401"""
    client = TestClient(app)
    
    # Test protected content endpoint
    response = client.get("/api/v1/content")
    assert response.status_code == 401
    
    # Test protected user endpoint
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_invalid_content_id(client):
    """Test accessing non-existent content"""
    # Register and login
    client.post("/api/v1/auth/register", json={
        "username": "testuser", 
        "email": "test@example.com", 
        "password": "TestPass123"
    })
    
    login_response = client.post("/api/v1/auth/token", data={
        "username": "testuser", 
        "password": "TestPass123"
    })
    token = login_response.json()["access_token"]
    
    # Try to get non-existent content
    response = client.get("/api/v1/content/99999", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 404
