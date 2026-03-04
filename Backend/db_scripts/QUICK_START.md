# Database Setup - Quick Start Guide

## 🚀 Fastest Way to Setup

### Windows Users

```cmd
cd Backend\db_scripts
setup_database.bat
```

### Linux/macOS Users

```bash
cd Backend/db_scripts
chmod +x setup_database.sh
./setup_database.sh
```

---

## 📋 Manual Setup (3 Steps)

### Step 1: Create Database
```bash
psql -U postgres -f 01_create_database.sql
```

### Step 2: Create Tables
```bash
psql -U postgres -d legal_assist -f 02_create_tables.sql
```

### Step 3: Seed Data
```bash
psql -U postgres -d legal_assist -f 03_seed_data.sql
```

---

## ✅ Verify Setup

### Check Tables
```bash
psql -U postgres -d legal_assist -c "\dt"
```

### Check Data
```bash
psql -U postgres -d legal_assist -c "SELECT COUNT(*) FROM documents;"
```

---

## 🔧 Update .env File

Edit `Backend/.env`:

```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/legal_assist
```

---

## 🎯 Test the System

### 1. Start Backend
```bash
cd Backend
python -m uvicorn app.main:app --reload
```

### 2. Open Swagger UI
```
http://localhost:8000/docs
```

### 3. Test RAG Query
```json
POST /rag/query
{
  "query": "What is Section 302 of IPC?",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "top_k": 5
}
```

---

## 📚 What Gets Created

### Tables (9 total)
- ✅ roles (2 roles)
- ✅ users (2 sample users)
- ✅ categories (4 categories)
- ✅ documents (3 sample documents)
- ✅ document_embeddings (for vector search)
- ✅ conversations (for chat history)
- ✅ messages (for chat messages)
- ✅ user_activities (for analytics)
- ✅ search_history (for search tracking)

### Sample Data
- 2 Roles: admin, user
- 2 Users: Admin User, Test User
- 4 Categories: IPC, Insurance, Contract, Property
- 3 Documents: IPC sections, insurance guide

### Test User
```
ID: 123e4567-e89b-12d3-a456-426614174000
Name: Test User
Role: user
```

Use this ID for all API testing!

---

## 🐛 Common Issues

### Issue: "extension vector does not exist"
**Fix:** Install pgvector
```bash
# Ubuntu/Debian
sudo apt install postgresql-14-pgvector

# macOS
brew install pgvector
```

### Issue: "database does not exist"
**Fix:** Create manually
```bash
psql -U postgres -c "CREATE DATABASE legal_assist;"
```

### Issue: "permission denied"
**Fix:** Run as postgres user
```bash
sudo -u postgres psql -f 01_create_database.sql
```

---

## 🔄 Reset Database

To start fresh:

```bash
psql -U postgres -d legal_assist -f 05_cleanup.sql
```

Then run setup again.

---

## 📖 Need More Help?

- Read: `README.md` (detailed documentation)
- Check: `../API_TESTING_GUIDE.md` (API testing)
- Visit: http://localhost:8000/docs (Swagger UI)

---

**Ready to go!** 🎉
