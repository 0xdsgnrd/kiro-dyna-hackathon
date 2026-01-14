#!/usr/bin/env python3
"""
Test script for authentication endpoints
Run with: python test_auth.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_register():
    print("\nTesting user registration...")
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    print("✓ Registration successful")
    return response.json()

def test_duplicate_registration():
    print("\nTesting duplicate registration...")
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 400
    print("✓ Duplicate registration rejected")

def test_login():
    print("\nTesting login...")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/token", data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("✓ Login successful")
    return response.json()["access_token"]

def test_invalid_login():
    print("\nTesting invalid login...")
    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/token", data=data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 401
    print("✓ Invalid login rejected")

if __name__ == "__main__":
    print("=" * 60)
    print("Authentication API Tests")
    print("=" * 60)
    print("\nMake sure the backend is running:")
    print("cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
    print("\n" + "=" * 60)
    
    try:
        test_health()
        test_register()
        test_duplicate_registration()
        test_login()
        test_invalid_login()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
