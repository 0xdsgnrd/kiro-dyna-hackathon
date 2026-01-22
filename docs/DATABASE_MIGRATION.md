# Database Migration and Management Guide

## Overview

This guide covers database migration from SQLite to PostgreSQL for production deployment, including connection pooling, health monitoring, and performance optimization.

## Migration Process

### 1. Automatic Migration (Recommended)

The migration is handled automatically during deployment via the CI/CD pipeline:

```bash
# This runs automatically in the GitHub Actions workflow
python -m app.db.migrate create
python -m app.db.migrate migrate ./app.db  # if SQLite exists
```

### 2. Manual Migration

For manual migration or troubleshooting:

```bash
cd backend

# Set environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
export SQLITE_DB_PATH="./app.db"  # optional, defaults to ./app.db

# Run migration script
./migrations/migrate_to_postgres.sh
```

### 3. Individual Migration Commands

```bash
# Test database connection
python -m app.db.migrate check

# Create all tables
python -m app.db.migrate create

# Migrate data from SQLite
python -m app.db.migrate migrate ./app.db

# Test connection pool
python -m app.db.migrate pool
```

## Database Configuration

### Development (SQLite)
```bash
DATABASE_URL=sqlite:///./app.db
ENVIRONMENT=development
```

### Production (PostgreSQL)
```bash
DATABASE_URL=postgresql://user:password@host:5432/database
ENVIRONMENT=production
POSTGRES_HOST=your-rds-endpoint.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DB=contentdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
```

## Connection Pooling

Production configuration includes optimized connection pooling:

- **Pool Size**: 10 connections
- **Max Overflow**: 20 additional connections
- **Pool Recycle**: 1 hour (3600 seconds)
- **Pre-ping**: Validates connections before use
- **Pool Timeout**: 30 seconds

## Health Monitoring

### Health Check Endpoints

```bash
# Basic health check
curl https://your-api.com/health

# Detailed health check with database status
curl https://your-api.com/health/detailed
```

### Health Check Response

```json
{
  "status": "healthy",
  "database": {
    "connection": true,
    "tables": {
      "users": {"exists": true, "count": 5},
      "contents": {"exists": true, "count": 23},
      "tags": {"exists": true, "count": 12}
    },
    "performance": {
      "response_time_ms": 45.2,
      "status": "healthy"
    }
  },
  "version": "1.0.0",
  "environment": "production"
}
```

## Migration Safety

### Backup Strategy
- SQLite database is automatically backed up before migration
- Backup filename includes timestamp: `app.db.backup.20260120_133000`
- PostgreSQL backups handled by AWS RDS automated backups

### Data Integrity
- Migration preserves all foreign key relationships
- Tables migrated in dependency order to avoid constraint violations
- Transaction-based migration ensures atomicity

### Rollback Procedure
```bash
# If migration fails, restore from backup
cp app.db.backup.TIMESTAMP app.db

# Or restore PostgreSQL from RDS backup
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier restored-db \
  --db-snapshot-identifier your-snapshot-id
```

## Performance Optimization

### Database Indexes
All models include appropriate indexes:
- Primary keys (automatic)
- Foreign keys (automatic)
- User ID indexes for content isolation
- Search-optimized indexes on title and content fields

### Query Optimization
- Connection pooling reduces connection overhead
- Pre-ping prevents stale connection errors
- Pool recycling prevents long-running connection issues
- Lazy loading for relationships

### Monitoring Queries
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   ```bash
   # Check security groups allow port 5432
   # Verify RDS endpoint is correct
   # Test connection manually
   psql -h your-rds-endpoint -U postgres -d contentdb
   ```

2. **Migration Fails**
   ```bash
   # Check logs for specific error
   python -m app.db.migrate create 2>&1 | tee migration.log
   
   # Verify all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Performance Issues**
   ```bash
   # Check connection pool status
   python -m app.db.migrate pool
   
   # Monitor database performance
   curl https://your-api.com/health/detailed
   ```

4. **Table Creation Errors**
   ```bash
   # Drop and recreate tables (CAUTION: data loss)
   python -c "from app.db.session import engine, Base; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"
   ```

### Useful Commands

```bash
# Connect to production database
psql $DATABASE_URL

# Check database size
psql $DATABASE_URL -c "SELECT pg_size_pretty(pg_database_size('contentdb'));"

# List all tables
psql $DATABASE_URL -c "\dt"

# Check table row counts
psql $DATABASE_URL -c "SELECT schemaname,tablename,n_tup_ins-n_tup_del as rowcount FROM pg_stat_user_tables ORDER BY rowcount DESC;"
```

## Security Considerations

- Database credentials stored in AWS Secrets Manager
- SSL/TLS encryption for all database connections
- VPC security groups restrict database access
- Regular security updates via RDS maintenance windows
- Connection pooling prevents connection exhaustion attacks

## Maintenance

### Regular Tasks
- Monitor connection pool usage
- Review slow query logs
- Update database statistics
- Check backup integrity
- Monitor disk space usage

### Automated Maintenance
- AWS RDS handles OS updates
- Automated backups with 7-day retention
- Performance Insights for query monitoring
- CloudWatch metrics for system monitoring
