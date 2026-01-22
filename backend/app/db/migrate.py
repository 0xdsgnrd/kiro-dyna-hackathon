"""
Database migration utilities for production deployment
"""
import os
import sys
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.session import Base
from app.models import user, content, tag, category, content_source, user_preferences

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all tables in the database"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        logger.info(f"Creating tables in database: {settings.DATABASE_URL}")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def check_database_connection():
    """Test database connection"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def migrate_sqlite_to_postgres(sqlite_path: str):
    """Migrate data from SQLite to PostgreSQL"""
    import sqlite3
    
    if not os.path.exists(sqlite_path):
        logger.warning(f"SQLite database not found at {sqlite_path}")
        return True
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        # Connect to PostgreSQL
        pg_engine = create_engine(settings.DATABASE_URL)
        
        logger.info("Starting data migration from SQLite to PostgreSQL")
        
        # Define table migration order (respecting foreign keys)
        tables_order = ['users', 'categories', 'content_sources', 'tags', 'contents', 'content_tags', 'user_preferences']
        
        with pg_engine.connect() as pg_conn:
            for table_name in tables_order:
                logger.info(f"Migrating table: {table_name}")
                
                # Check if table exists in SQLite
                cursor = sqlite_conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                if not cursor.fetchone():
                    logger.info(f"Table {table_name} not found in SQLite, skipping")
                    continue
                
                # Get data from SQLite
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if not rows:
                    logger.info(f"No data in table {table_name}")
                    continue
                
                # Get column names
                columns = [description[0] for description in cursor.description]
                
                # Clear existing data in PostgreSQL
                pg_conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
                
                # Insert data
                placeholders = ', '.join([f':{col}' for col in columns])
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                
                # Convert rows to dictionaries
                data = [dict(zip(columns, row)) for row in rows]
                
                # Execute batch insert
                pg_conn.execute(text(insert_sql), data)
                pg_conn.commit()
                
                logger.info(f"Migrated {len(rows)} rows to {table_name}")
        
        sqlite_conn.close()
        logger.info("Data migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

def setup_connection_pool():
    """Configure database connection pool for production"""
    try:
        from sqlalchemy.pool import QueuePool
        
        engine = create_engine(
            settings.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        logger.info("Connection pool configured successfully")
        return engine
        
    except Exception as e:
        logger.error(f"Failed to setup connection pool: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate.py <command>")
        print("Commands:")
        print("  check - Test database connection")
        print("  create - Create all tables")
        print("  migrate <sqlite_path> - Migrate from SQLite")
        print("  pool - Test connection pool")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        success = check_database_connection()
        sys.exit(0 if success else 1)
    
    elif command == "create":
        success = create_tables()
        sys.exit(0 if success else 1)
    
    elif command == "migrate":
        if len(sys.argv) < 3:
            print("Error: SQLite path required for migrate command")
            sys.exit(1)
        sqlite_path = sys.argv[2]
        success = migrate_sqlite_to_postgres(sqlite_path)
        sys.exit(0 if success else 1)
    
    elif command == "pool":
        engine = setup_connection_pool()
        sys.exit(0 if engine else 1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
