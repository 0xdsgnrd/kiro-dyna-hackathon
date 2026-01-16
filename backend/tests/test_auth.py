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
