#!/usr/bin/env python3
"""
Test script for Phase 2 content endpoints
Run backend server first: uvicorn app.main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_content_endpoints():
    print("🧪 Testing Phase 2 Content Endpoints\n")
    
    # 1. Register a test user
    print("1️⃣ Registering test user...")
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ User registered successfully")
        elif response.status_code == 400:
            print("ℹ️  User already exists, continuing...")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 2. Login to get token
    print("\n2️⃣ Logging in...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 3. Create a category
    print("\n3️⃣ Creating category...")
    category_data = {
        "name": "Tech Articles",
        "description": "Technology related articles"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/categories", json=category_data, headers=headers)
        if response.status_code == 201:
            category = response.json()
            category_id = category["id"]
            print(f"✅ Category created: {category['name']} (ID: {category_id})")
        else:
            print(f"❌ Category creation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 4. Create tags
    print("\n4️⃣ Creating tags...")
    tag_names = ["python", "fastapi", "tutorial"]
    tag_ids = []
    
    for tag_name in tag_names:
        try:
            response = requests.post(f"{BASE_URL}/tags", json={"name": tag_name}, headers=headers)
            if response.status_code == 201:
                tag = response.json()
                tag_ids.append(tag["id"])
                print(f"✅ Tag created: {tag['name']} (ID: {tag['id']})")
        except Exception as e:
            print(f"❌ Error creating tag {tag_name}: {e}")
    
    # 5. Create content
    print("\n5️⃣ Creating content...")
    content_data = {
        "title": "FastAPI Tutorial",
        "url": "https://fastapi.tiangolo.com",
        "content_text": "Learn how to build APIs with FastAPI",
        "content_type": "article",
        "category_id": category_id,
        "tag_ids": tag_ids
    }
    
    try:
        response = requests.post(f"{BASE_URL}/content", json=content_data, headers=headers)
        if response.status_code == 201:
            content = response.json()
            content_id = content["id"]
            print(f"✅ Content created: {content['title']} (ID: {content_id})")
            print(f"   Tags: {[tag['name'] for tag in content['tags']]}")
            print(f"   Category: {content['category']['name']}")
        else:
            print(f"❌ Content creation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 6. List content
    print("\n6️⃣ Listing all content...")
    try:
        response = requests.get(f"{BASE_URL}/content", headers=headers)
        if response.status_code == 200:
            contents = response.json()
            print(f"✅ Found {len(contents)} content item(s)")
            for c in contents:
                print(f"   - {c['title']} ({c['content_type']})")
        else:
            print(f"❌ List failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 7. Search content
    print("\n7️⃣ Searching content...")
    try:
        response = requests.get(f"{BASE_URL}/content/search?q=FastAPI", headers=headers)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Found {len(results)} result(s) for 'FastAPI'")
        else:
            print(f"❌ Search failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 8. Update content
    print("\n8️⃣ Updating content...")
    update_data = {
        "title": "FastAPI Tutorial - Updated",
        "content_text": "Learn how to build modern APIs with FastAPI"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/content/{content_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            updated = response.json()
            print(f"✅ Content updated: {updated['title']}")
        else:
            print(f"❌ Update failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 9. Get single content
    print("\n9️⃣ Getting single content...")
    try:
        response = requests.get(f"{BASE_URL}/content/{content_id}", headers=headers)
        if response.status_code == 200:
            content = response.json()
            print(f"✅ Retrieved: {content['title']}")
        else:
            print(f"❌ Get failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✨ All tests completed!")

if __name__ == "__main__":
    test_content_endpoints()
