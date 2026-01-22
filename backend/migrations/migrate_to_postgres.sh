#!/bin/bash

# Database migration script for production deployment
# This script migrates data from SQLite to PostgreSQL

set -e

echo "Starting database migration..."

# Check if required environment variables are set
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL environment variable must be set"
    exit 1
fi

# Set default SQLite path if not provided
SQLITE_DB_PATH=${SQLITE_DB_PATH:-"./app.db"}

echo "Using SQLite database: $SQLITE_DB_PATH"
echo "Target PostgreSQL: $DATABASE_URL"

# Create backup of SQLite database if it exists
if [ -f "$SQLITE_DB_PATH" ]; then
    echo "Creating backup of SQLite database..."
    cp "$SQLITE_DB_PATH" "${SQLITE_DB_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Backup created successfully"
else
    echo "No SQLite database found at $SQLITE_DB_PATH - will create fresh PostgreSQL database"
fi

# Run migration using Python script
echo "Running database migration..."
python3 -m app.db.migrate check
if [ $? -ne 0 ]; then
    echo "Error: Cannot connect to PostgreSQL database"
    exit 1
fi

echo "Creating database tables..."
python3 -m app.db.migrate create
if [ $? -ne 0 ]; then
    echo "Error: Failed to create database tables"
    exit 1
fi

# Migrate data if SQLite database exists
if [ -f "$SQLITE_DB_PATH" ]; then
    echo "Migrating data from SQLite to PostgreSQL..."
    python3 -m app.db.migrate migrate "$SQLITE_DB_PATH"
    if [ $? -ne 0 ]; then
        echo "Error: Data migration failed"
        exit 1
    fi
    echo "Data migration completed successfully"
else
    echo "No existing data to migrate - fresh database ready"
fi

# Test connection pool
echo "Testing connection pool configuration..."
python3 -m app.db.migrate pool
if [ $? -ne 0 ]; then
    echo "Warning: Connection pool test failed, but migration completed"
    exit 0
fi

echo "Database migration completed successfully!"
echo "PostgreSQL database is ready for production use"
