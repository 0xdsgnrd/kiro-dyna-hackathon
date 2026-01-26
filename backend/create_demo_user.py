#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_demo_user():
    db = SessionLocal()
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.username == "demo").first()
        if existing_user:
            print("Demo user already exists")
            return
        
        # Create demo user
        hashed_password = get_password_hash("demo123")
        demo_user = User(
            username="demo",
            email="demo@example.com",
            hashed_password=hashed_password
        )
        
        db.add(demo_user)
        db.commit()
        print("Demo user created successfully!")
        print("Username: demo")
        print("Password: demo123")
        
    except Exception as e:
        print(f"Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
