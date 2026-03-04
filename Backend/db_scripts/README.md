# Database Setup Scripts

SQL scripts for setting up the Legal Assistant database from scratch.

## Prerequisites

1. **PostgreSQL 12+** installed and running
2. **pgvector extension** installed ([Installation Guide](https://github.com/pgvector/pgvector))
3. PostgreSQL user with database creation privileges

## Quick Start

### Option 1: Automated Setup (Recommended)

Run all scripts in order:

```bash
# Navigate to db_scripts directory
cd Backend/db_scripts

# Run all setup scripts
psql -U postgres -f 01_create_database.sql
psql -U postgres -d legal_assist -f 02_create_tables.sql
psql -U postgres -d legal_assist -f 03_seed_data.sql
```

### Option 2: Manual Setup

Run each script individually:

```bash
# 1. Create database and enable extensions
psql -U postgres -f 01_create_database.sql

# 2. Create all tables
psql -U postgres -d legal_assist -f 02_create_tables.sql

# 3. Seed initial data
psql -U postgres -d legal_assist -f 03_seed_data.sql

# 4. (Optional) Check embedding status
psql -U postgres -d legal_assist -f 04_generate_embeddings.sql
```

## Script Details

### 01_create_database.sql
**Purpose:** Creates the database and enables required extensions

**What it does:**
- Creates `legal_assist` database
- Enables `uuid-ossp` extension (for UUID generation)
- Enables `vector` extension (for pgvector support)

**Run as:** PostgreSQL superuser (e.g., `postgres`)

---

### 02_create_tables.sql
**Purpose:** Creates all database tables and indexes

**Tables created:**
- `roles` - User roles (admin, user)
- `users` - Application users
- `categories` - Document categories
- `documents` - Legal documents
- `document_embeddings` - Vector embeddings (768 dimensions)
- `conversations` - Chat conversations
- `messages` - Chat messages
- `user_activities` - User activity tracking
- `search_history` - Search query history

**Indexes created:**
- Performance indexes on foreign keys
- GIN index on document tags
- IVFFlat index on embeddings for vector search
- Full-text search index on search queries

---

### 03_seed_data.sql
**Purpose:** Populates initial data for testing

**Data seeded:**
- 2 roles: `admin`, `user`
- 2 sample users (including test user)
- 4 sample categories (IPC, Insurance, Contract, Property)
- 3 sample documents (IPC sections, insurance guide)

**Test User ID:** `123e4567-e89b-12d3-a456-426614174000`

---

### 04_generate_embeddings.sql
**Purpose:** Check embedding status and provide generation instructions

**What it does:**
- Lists documents without embeddings
- Shows embedding statistics
- Provides instructions for generating embeddings

**Note:** Embeddings are generated automatically by the backend, not by SQL.

---

### 05_cleanup.sql
**Purpose:** Reset the database (delete all data)

**⚠️ WARNING:** This script drops all tables and data!

**Use cases:**
- Development environment reset
- Testing fresh installation
- Removing all data before redeployment

---

## Database Schema Overview

```
roles
  ├── users
  │     ├── documents (created_by)
  │     ├── conversations
  │     ├── user_activities
  │     └── search_history
  │
  └── categories
        └── documents
              ├── document_embeddings (1:1)
              ├── user_activities
              └── search_history

conversations
  └── messages

documents
  ├── document_embeddings (vector search)
  ├── user_activities
  └── search_history
```

## After Database Setup

### 1. Update Environment Variables

Edit `Backend/.env`:

```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/legal_assist
```

### 2. Generate Embeddings

Embeddings are generated automatically when documents are created via the API. For existing documents:

```bash
cd Backend
python app/scripts/generate_embeddings_batch.py
```

Or use the API:
```bash
POST http://localhost:8000/embeddings/generate-batch
```

### 3. Start the Backend

```bash
cd Backend
python -m uvicorn app.main:app --reload
```

### 4. Verify Setup

Visit: http://localhost:8000/docs

Test endpoints:
- `GET /health` - Application health
- `GET /rag/health` - RAG system health
- `GET /categories/` - List categories
- `GET /documents/` - List documents

## Troubleshooting

### Issue: "extension vector does not exist"

**Solution:** Install pgvector extension

```bash
# Ubuntu/Debian
sudo apt install postgresql-14-pgvector

# macOS (Homebrew)
brew install pgvector

# Or build from source
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### Issue: "database legal_assist does not exist"

**Solution:** Create database manually

```bash
psql -U postgres -c "CREATE DATABASE legal_assist;"
```

### Issue: "permission denied to create extension"

**Solution:** Run as PostgreSQL superuser

```bash
psql -U postgres -d legal_assist -c "CREATE EXTENSION vector;"
```

### Issue: "relation already exists"

**Solution:** Tables already exist. Either:
1. Skip table creation (safe)
2. Drop and recreate (use `05_cleanup.sql`)

### Issue: Embeddings not generating

**Solution:** Check:
1. Backend is running
2. Documents exist in database
3. Embedding model is downloaded
4. Check logs: `tail -f backend.log`

## Maintenance Scripts

### Check Database Size

```sql
SELECT 
    pg_size_pretty(pg_database_size('legal_assist')) as database_size;
```

### Check Table Sizes

```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Check Embedding Coverage

```sql
SELECT 
    COUNT(*) as total_docs,
    COUNT(de.document_id) as with_embeddings,
    COUNT(*) - COUNT(de.document_id) as missing_embeddings
FROM documents d
LEFT JOIN document_embeddings de ON d.id = de.document_id
WHERE d.deleted_at IS NULL;
```

### Vacuum and Analyze

```sql
VACUUM ANALYZE;
```

## Migration from Alembic

If you're using Alembic migrations instead of these SQL scripts:

```bash
cd Backend

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Check current version
alembic current
```

## Backup and Restore

### Backup Database

```bash
pg_dump -U postgres legal_assist > backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
psql -U postgres legal_assist < backup_20240304.sql
```

### Backup with Compression

```bash
pg_dump -U postgres -Fc legal_assist > backup_$(date +%Y%m%d).dump
```

### Restore from Compressed Backup

```bash
pg_restore -U postgres -d legal_assist backup_20240304.dump
```

## Production Considerations

1. **Change default passwords** in seed data
2. **Remove test users** before production
3. **Set up regular backups** (daily recommended)
4. **Configure connection pooling** (e.g., PgBouncer)
5. **Monitor database performance** (pg_stat_statements)
6. **Set up replication** for high availability
7. **Configure SSL** for database connections
8. **Implement proper access control** (roles and permissions)

## Support

For issues or questions:
- Check the main README.md
- Review API documentation at `/docs`
- Check application logs
- Verify PostgreSQL logs: `/var/log/postgresql/`

---

**Last Updated:** March 2024  
**Database Version:** PostgreSQL 12+  
**pgvector Version:** 0.5.0+
