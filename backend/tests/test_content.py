import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, Base, engine

client = TestClient(app)

# Test fixtures
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_token():
    # Register and login user
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    })
    response = client.post("/api/v1/auth/token", data={
        "username": "testuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]

@pytest.fixture
def auth_token2():
    # Register and login second user
    client.post("/api/v1/auth/register", json={
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "testpass123"
    })
    response = client.post("/api/v1/auth/token", data={
        "username": "testuser2",
        "password": "testpass123"
    })
    return response.json()["access_token"]

# Content CRUD Tests
def test_create_content_full(auth_token):
    response = client.post(
        "/api/v1/content",
        json={
            "title": "Test Article",
            "url": "https://example.com/article",
            "content_text": "This is test content",
            "content_type": "article",
            "tag_ids": []
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["content_type"] == "article"
    assert "id" in data

def test_create_content_minimal(auth_token):
    response = client.post(
        "/api/v1/content",
        json={
            "title": "Minimal Content",
            "content_type": "note"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Content"

def test_list_content(auth_token):
    # Create test content
    client.post(
        "/api/v1/content",
        json={"title": "Content 1", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/v1/content",
        json={"title": "Content 2", "content_type": "video"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/v1/content",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_content(auth_token):
    # Create content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "Test Content", "content_type": "note"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # Get content
    response = client.get(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Content"

def test_update_content(auth_token):
    # Create content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "Original Title", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # Update content
    response = client.put(
        f"/api/v1/content/{content_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_delete_content(auth_token):
    # Create content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "To Delete", "content_type": "note"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # Delete content
    response = client.delete(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204
    
    # Verify deleted
    get_response = client.get(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404

# User Isolation Tests
def test_user_cannot_access_other_content(auth_token, auth_token2):
    # User 1 creates content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "User 1 Content", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # User 2 tries to access
    response = client.get(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {auth_token2}"}
    )
    assert response.status_code == 404

def test_user_cannot_update_other_content(auth_token, auth_token2):
    # User 1 creates content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "User 1 Content", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # User 2 tries to update
    response = client.put(
        f"/api/v1/content/{content_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {auth_token2}"}
    )
    assert response.status_code == 404

def test_user_cannot_delete_other_content(auth_token, auth_token2):
    # User 1 creates content
    create_response = client.post(
        "/api/v1/content",
        json={"title": "User 1 Content", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    content_id = create_response.json()["id"]
    
    # User 2 tries to delete
    response = client.delete(
        f"/api/v1/content/{content_id}",
        headers={"Authorization": f"Bearer {auth_token2}"}
    )
    assert response.status_code == 404

# Search and Filtering Tests
def test_search_by_title(auth_token):
    client.post(
        "/api/v1/content",
        json={"title": "Python Tutorial", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/v1/content",
        json={"title": "JavaScript Guide", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/v1/content/search?q=Python",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Python" in data[0]["title"]

def test_search_by_content_text(auth_token):
    client.post(
        "/api/v1/content",
        json={
            "title": "Article 1",
            "content_text": "This talks about Python programming",
            "content_type": "article"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/v1/content/search?q=Python",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_filter_by_content_type(auth_token):
    client.post(
        "/api/v1/content",
        json={"title": "Article", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/v1/content",
        json={"title": "Video", "content_type": "video"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/v1/content/search?content_type=article",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content_type"] == "article"

def test_sort_by_title(auth_token):
    client.post(
        "/api/v1/content",
        json={"title": "Zebra", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/v1/content",
        json={"title": "Apple", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/v1/content/search?sort_by=title&sort_order=asc",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Apple"
    assert data[1]["title"] == "Zebra"

# Tags and Categories Tests
def test_content_with_tags(auth_token):
    # Create tag
    tag_response = client.post(
        "/api/v1/tags",
        json={"name": "python"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    tag_id = tag_response.json()["id"]
    
    # Create content with tag
    response = client.post(
        "/api/v1/content",
        json={
            "title": "Python Article",
            "content_type": "article",
            "tag_ids": [tag_id]
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "python"

def test_content_with_category(auth_token):
    # Create category
    cat_response = client.post(
        "/api/v1/categories",
        json={"name": "Programming", "description": "Programming articles"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    cat_id = cat_response.json()["id"]
    
    # Create content with category
    response = client.post(
        "/api/v1/content",
        json={
            "title": "Code Article",
            "content_type": "article",
            "category_id": cat_id
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category"]["name"] == "Programming"

def test_filter_by_tag(auth_token):
    # Create tag
    tag_response = client.post(
        "/api/v1/tags",
        json={"name": "tutorial"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    tag_id = tag_response.json()["id"]
    
    # Create content with and without tag
    client.post(
        "/api/v1/content",
        json={"title": "Tagged", "content_type": "article", "tag_ids": [tag_id]},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    client.post(
        "/api/v1/content",
        json={"title": "Untagged", "content_type": "article"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Search by tag
    response = client.get(
        f"/api/v1/content/search?tag_id={tag_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Tagged"

# Error Handling Tests
def test_create_content_without_auth():
    response = client.post(
        "/api/v1/content",
        json={"title": "Test", "content_type": "article"}
    )
    assert response.status_code == 401

def test_create_content_invalid_type(auth_token):
    response = client.post(
        "/api/v1/content",
        json={"title": "Test", "content_type": "invalid"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422

def test_get_nonexistent_content(auth_token):
    response = client.get(
        "/api/v1/content/99999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
