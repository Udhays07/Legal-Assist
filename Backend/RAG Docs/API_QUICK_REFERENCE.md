# API Quick Reference Card

## Base URL
```
http://localhost:8000
```

## Test User UUID
```
123e4567-e89b-12d3-a456-426614174000
```

---

## 🔥 Most Used Endpoints

### 1. Ask a Question (RAG)
```bash
POST /rag/query
{
  "query": "Your question here",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "top_k": 5,
  "include_sources": true
}
```

### 2. Search Documents
```bash
POST /rag/search
{
  "query": "search term",
  "top_k": 5,
  "min_similarity": 0.5
}
```

### 3. Create Document
```bash
POST /documents/
Form Data:
- category_id: {uuid}
- title: "Document Title"
- content: "Document content..."
- tags: ["tag1", "tag2"]
- status: "published"
```

### 4. Create Category
```bash
POST /categories/
{
  "title": "Category Name",
  "description": "Description",
  "is_active": true
}
```

---

## 📋 Complete Endpoint List

### RAG System
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/rag/query` | Ask question, get AI answer |
| POST | `/rag/search` | Semantic search only |
| GET | `/rag/conversations?user_id={uuid}` | List conversations |
| GET | `/rag/conversations/{id}?user_id={uuid}` | Get conversation history |
| POST | `/rag/feedback?message_id={uuid}` | Submit feedback |
| GET | `/rag/health` | Check RAG health |

### Documents
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/documents/` | Create document |
| GET | `/documents/` | List all documents |
| GET | `/documents/?category_id={uuid}` | Filter by category |
| GET | `/documents/{id}` | Get single document |
| PUT | `/documents/{id}` | Update document |
| DELETE | `/documents/{id}` | Delete document |

### Categories
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/categories/` | Create category |
| GET | `/categories/` | List categories |
| GET | `/categories/{id}` | Get single category |
| PUT | `/categories/{id}` | Update category |
| DELETE | `/categories/{id}` | Delete category |

### Health
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | App health |
| GET | `/rag/health` | RAG system health |

---

## 🎯 Common Query Parameters

### RAG Query
- `query` (required): Your question
- `user_id` (required): User UUID
- `conversation_id` (optional): For follow-ups
- `top_k` (optional): Number of docs (default: 5)
- `min_similarity` (optional): Threshold 0-1 (default: 0.3)
- `category_id` (optional): Filter by category
- `include_sources` (optional): Include sources (default: true)

### Search
- `query` (required): Search term
- `top_k` (optional): Results count (default: 5)
- `min_similarity` (optional): Threshold (default: 0.0)
- `category_id` (optional): Filter by category
- `status` (optional): "published" or "draft"

---

## 📊 Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted (no content) |
| 400 | Bad request |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

---

## 🔧 cURL Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Create Category
```bash
curl -X POST http://localhost:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"title":"IPC","description":"Indian Penal Code","is_active":true}'
```

### Create Document
```bash
curl -X POST http://localhost:8000/documents/ \
  -F "category_id=YOUR_UUID" \
  -F "title=Section 302" \
  -F "content=Punishment for murder..." \
  -F "tags=[\"ipc\"]" \
  -F "status=published"
```

### RAG Query
```bash
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query":"What is Section 302?",
    "user_id":"123e4567-e89b-12d3-a456-426614174000",
    "top_k":5
  }'
```

### Search
```bash
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"insurance","top_k":5}'
```

---

## 🐍 Python Examples

### RAG Query
```python
import requests

response = requests.post(
    "http://localhost:8000/rag/query",
    json={
        "query": "What is Section 302?",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "top_k": 5
    }
)
print(response.json()["answer"])
```

### Create Document
```python
import requests

response = requests.post(
    "http://localhost:8000/documents/",
    data={
        "category_id": "your-uuid",
        "title": "Document Title",
        "content": "Document content...",
        "tags": '["tag1", "tag2"]',
        "status": "published"
    }
)
print(response.json())
```

---

## 📱 Postman Quick Setup

1. Import `Legal_Assistant_API.postman_collection.json`
2. Set variables:
   - `base_url`: `http://localhost:8000`
   - `user_id`: `123e4567-e89b-12d3-a456-426614174000`
3. Run "Create Category" → saves `category_id`
4. Run "Create Document" → saves `document_id`
5. Run "RAG Query" → saves `conversation_id`
6. Test other endpoints!

---

## 🎨 Interactive Documentation

### Swagger UI (Best for Testing)
```
http://localhost:8000/docs
```
- Click "Try it out" on any endpoint
- Fill in parameters
- Click "Execute"
- See response immediately!

### ReDoc (Best for Reading)
```
http://localhost:8000/redoc
```
- Beautiful, readable documentation
- Search functionality
- Code examples

---

## ⚡ Performance Tips

### First Request
- Takes ~2-3 seconds (model loading)
- Subsequent requests: ~100-300ms

### Optimize Queries
- Use `min_similarity` to filter results
- Lower `top_k` for faster responses
- Use `category_id` to narrow search

### Monitor Performance
- Check `processing_time_ms` in responses
- RAG queries: 200-500ms typical
- Search only: 100-200ms typical

---

## 🚨 Common Errors

### "Module not found"
```bash
cd Backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### "Database connection failed"
Check `.env` file:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/legal_assist
```

### "LLM service unavailable"
Check `.env` file:
```
GROQ_API_KEY=your-key-here
LLM_MODEL=llama-3.1-8b-instant
```

### "No documents found"
1. Create a category first
2. Create documents with that category_id
3. Wait a moment for embeddings to generate

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `api_documentation.yaml` | OpenAPI spec (import to tools) |
| `Legal_Assistant_API.postman_collection.json` | Postman collection |
| `API_TESTING_GUIDE.md` | Detailed testing guide |
| `API_README.md` | Complete API overview |
| `API_QUICK_REFERENCE.md` | This file! |

---

## 🎯 5-Minute Test

```bash
# 1. Start server
cd Backend
python -m uvicorn app.main:app --reload

# 2. Check health
curl http://localhost:8000/health

# 3. Open browser
open http://localhost:8000/docs

# 4. Try "POST /rag/query" with:
{
  "query": "What is Section 302 of IPC?",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}

# 5. Done! 🎉
```

---

**Need Help?**
- Check `/docs` for interactive testing
- Read `API_TESTING_GUIDE.md` for detailed examples
- Review `API_README.md` for troubleshooting

**Happy Testing! 🚀**
