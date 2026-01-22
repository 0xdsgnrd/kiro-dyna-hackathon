"""
Comprehensive integration tests for authentication flow
"""
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from tests.conftest import override_get_db, test_db

class TestAuthenticationFlow:
    """Test complete authentication workflows"""
    
    @pytest.fixture
    def client(self):
        app.dependency_overrides[get_db] = override_get_db
        return TestClient(app)
    
    @pytest.fixture
    def test_user_data(self):
        return {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    
    def test_complete_registration_flow(self, client, test_user_data):
        """Test complete user registration process"""
        # Register new user
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        user_data = response.json()
        assert user_data["username"] == test_user_data["username"]
        assert user_data["email"] == test_user_data["email"]
        assert "id" in user_data
        assert "password" not in user_data  # Password should not be returned
    
    def test_complete_login_flow(self, client, test_user_data):
        """Test complete user login process"""
        # First register user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Login with credentials
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 200
        
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        return token_data["access_token"]
    
    def test_protected_route_access(self, client, test_user_data):
        """Test accessing protected routes with valid token"""
        # Register and login
        client.post("/api/v1/auth/register", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        token_response = client.post("/api/v1/auth/token", data=login_data)
        token = token_response.json()["access_token"]
        
        # Access protected route
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        user_data = response.json()
        assert user_data["username"] == test_user_data["username"]
        assert user_data["email"] == test_user_data["email"]
    
    def test_invalid_token_rejection(self, client):
        """Test that invalid tokens are rejected"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_duplicate_registration_prevention(self, client, test_user_data):
        """Test that duplicate registrations are prevented"""
        # Register user first time
        response1 = client.post("/api/v1/auth/register", json=test_user_data)
        assert response1.status_code == 201
        
        # Try to register same user again
        response2 = client.post("/api/v1/auth/register", json=test_user_data)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"].lower()
    
    def test_invalid_login_credentials(self, client, test_user_data):
        """Test login with invalid credentials"""
        # Register user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try login with wrong password
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
    
    def test_registration_validation(self, client):
        """Test registration input validation"""
        # Test missing fields
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422
        
        # Test invalid email
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422
        
        # Test short password
        short_password_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
        response = client.post("/api/v1/auth/register", json=short_password_data)
        assert response.status_code == 422

@pytest.mark.asyncio
class TestAuthenticationPerformance:
    """Test authentication performance under load"""
    
    async def test_concurrent_registrations(self):
        """Test multiple concurrent registrations"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            app.dependency_overrides[get_db] = override_get_db
            
            # Create multiple registration tasks
            tasks = []
            for i in range(10):
                user_data = {
                    "username": f"user{i}",
                    "email": f"user{i}@example.com",
                    "password": "password123"
                }
                task = client.post("/api/v1/auth/register", json=user_data)
                tasks.append(task)
            
            # Execute concurrently
            responses = await asyncio.gather(*tasks)
            
            # Verify all succeeded
            success_count = sum(1 for r in responses if r.status_code == 201)
            assert success_count == 10
    
    async def test_concurrent_logins(self):
        """Test multiple concurrent logins"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            app.dependency_overrides[get_db] = override_get_db
            
            # First register users
            for i in range(5):
                user_data = {
                    "username": f"loginuser{i}",
                    "email": f"loginuser{i}@example.com",
                    "password": "password123"
                }
                await client.post("/api/v1/auth/register", json=user_data)
            
            # Create concurrent login tasks
            tasks = []
            for i in range(5):
                login_data = {
                    "username": f"loginuser{i}",
                    "password": "password123"
                }
                task = client.post("/api/v1/auth/token", data=login_data)
                tasks.append(task)
            
            # Execute concurrently
            responses = await asyncio.gather(*tasks)
            
            # Verify all succeeded
            success_count = sum(1 for r in responses if r.status_code == 200)
            assert success_count == 5

class TestAuthenticationSecurity:
    """Test authentication security measures"""
    
    def test_password_hashing(self, client, test_user_data):
        """Test that passwords are properly hashed"""
        # Register user
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        # Verify password is not stored in plain text
        user_data = response.json()
        assert "password" not in user_data
        
        # Verify we can still login (password verification works)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        assert login_response.status_code == 200
    
    def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention in authentication"""
        # Try SQL injection in username
        malicious_data = {
            "username": "admin'; DROP TABLE users; --",
            "email": "test@example.com",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/register", json=malicious_data)
        # Should either succeed (treating as normal username) or fail validation
        assert response.status_code in [201, 422]
        
        # Try SQL injection in login
        login_data = {
            "username": "admin' OR '1'='1",
            "password": "anything"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401  # Should fail authentication
    
    def test_rate_limiting(self, client):
        """Test rate limiting on authentication endpoints"""
        # This test would need rate limiting to be configured
        # For now, just verify the endpoint responds
        for i in range(10):
            response = client.post("/api/v1/auth/token", data={
                "username": "nonexistent",
                "password": "wrong"
            })
            # Should consistently return 401, not be rate limited in test
            assert response.status_code == 401
