def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "user1", "password": "pass123"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "user2", "password": "pass123"}
    )
    assert response.status_code == 400

def test_register_duplicate_username(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "username": "testuser", "password": "pass123"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user2@example.com", "username": "testuser", "password": "pass123"}
    )
    assert response.status_code == 400

def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 401

def test_get_current_user_success(client):
    """Test getting current user with valid token"""
    # Register and login
    client.post("/api/v1/auth/register", json={
        "username": "testuser2", 
        "email": "test2@example.com", 
        "password": "TestPass123"
    })
    
    login_response = client.post("/api/v1/auth/token", data={
        "username": "testuser2", 
        "password": "TestPass123"
    })
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    assert response.json()["username"] == "testuser2"

def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get("/api/v1/auth/me", headers={
        "Authorization": "Bearer invalid_token"
    })
    
    assert response.status_code == 401

def test_get_current_user_no_token(client):
    """Test getting current user without token"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401
