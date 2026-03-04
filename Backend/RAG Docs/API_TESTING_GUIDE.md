# API Testing Guide

Quick reference for testing the Legal Assistant Backend APIs.

## Base URL
```
http://localhost:8000
```

## Import OpenAPI Spec

### Option 1: Import into Postman
1. Open Postman
2. Click "Import" button
3. Select `api_documentation.yaml`
4. All endpoints will be automatically configured!

### Option 2: Use Swagger UI
1. Start the backend server
2. Visit: `http://localhost:8000/docs`
3. Interactive API documentation with "Try it out" buttons

### Option 3: Use ReDoc
1. Start the backend server
2. Visit: `http://localhost:8000/redoc`
3. Beautiful, readable API documentation

---

## Quick Test Sequence

### 1. Check System Health
```bash
GET http://localhost:8000/health
GET http://localhost:8000/rag/health
```

### 2. Create a Category
```bash
POST http://localhost:8000/categories/
Content-Type: application/json

{
  "title": "Indian Penal Code",
  "description": "Sections from IPC",
  "is_active": true
}
```
**Save the returned `id` as `CATEGORY_ID`**

### 3. Create a Document
```bash
POST http://localhost:8000/documents/
Content-Type: multipart/form-data

category_id: {CATEGORY_ID}
title: Section 302 IPC - Punishment for Murder
content: Section 302 of the Indian Penal Code deals with punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.
tags: ["ipc", "criminal law", "murder"]
status: published
```

### 4. Test RAG Query
```bash
POST http://localhost:8000/rag/query
Content-Type: application/json

{
  "query": "What is the punishment for murder under IPC?",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "conversation_id": null,
  "top_k": 5,
  "min_similarity": 0.3,
  "include_sources": true
}
```
**Save the returned `conversation_id` for follow-up questions**

### 5. Ask Follow-up Question
```bash
POST http://localhost:8000/rag/query
Content-Type: application/json

{
  "query": "What are the exceptions to this law?",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "conversation_id": "{CONVERSATION_ID_FROM_STEP_4}",
  "top_k": 5,
  "include_sources": true
}
```

### 6. View Conversation History
```bash
GET http://localhost:8000/rag/conversations/{CONVERSATION_ID}?user_id=123e4567-e89b-12d3-a456-426614174000
```

### 7. Submit Feedback
```bash
POST http://localhost:8000/rag/feedback?message_id={MESSAGE_ID}
Content-Type: application/json

{
  "rating": 5,
  "feedback": "Very helpful and accurate!"
}
```

---

## Test User UUID

For all testing, you can use this UUID:
```
123e4567-e89b-12d3-a456-426614174000
```

---

## Common Test Scenarios

### Scenario 1: Document Upload with File
```bash
POST http://localhost:8000/documents/
Content-Type: multipart/form-data

category_id: {CATEGORY_ID}
title: Insurance Policy Document
file: [Select PDF/DOCX/TXT file]
tags: ["insurance", "policy"]
status: published
```

### Scenario 2: Semantic Search Only
```bash
POST http://localhost:8000/rag/search
Content-Type: application/json

{
  "query": "insurance claims",
  "top_k": 10,
  "min_similarity": 0.5,
  "status": "published"
}
```

### Scenario 3: Filter Documents by Category
```bash
GET http://localhost:8000/documents/?category_id={CATEGORY_ID}&status=published
```

### Scenario 4: Update Document Content
```bash
PUT http://localhost:8000/documents/{DOCUMENT_ID}
Content-Type: application/json

{
  "content": "Updated content here...",
  "tags": ["updated", "revised"]
}
```
*Note: Embeddings are automatically regenerated when content is updated*

### Scenario 5: List All Conversations
```bash
GET http://localhost:8000/rag/conversations?user_id=123e4567-e89b-12d3-a456-426614174000&limit=20
```

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created successfully |
| 204 | Deleted successfully (no content) |
| 400 | Bad request (validation error) |
| 404 | Resource not found |
| 422 | Unprocessable entity (file type error, etc.) |
| 500 | Internal server error |

---

## Tips for Testing

### 1. Use Environment Variables in Postman
Create a Postman environment with:
- `base_url`: `http://localhost:8000`
- `user_id`: `123e4567-e89b-12d3-a456-426614174000`
- `category_id`: (set after creating category)
- `conversation_id`: (set after first query)

### 2. Check Logs
Monitor the backend terminal for detailed logs:
```bash
cd Backend
python -m uvicorn app.main:app --reload
```

### 3. Test Embeddings
After creating a document, verify embeddings were generated:
```sql
-- In PostgreSQL
SELECT document_id, 
       vector_dims(embedding) as dimensions,
       created_at 
FROM document_embeddings;
```

### 4. Test Similarity Search
Create multiple documents and test semantic search:
```bash
# Create documents about different topics
# Then search with related queries to see similarity scores
```

### 5. Monitor Performance
Check `processing_time_ms` in responses:
- First query: ~500-1000ms (model loading)
- Subsequent queries: ~100-300ms (cached model)

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Ensure you're in the Backend directory and virtual environment is activated
```bash
cd Backend
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Issue: "Database connection failed"
**Solution:** Check PostgreSQL is running and .env is configured
```bash
# Check .env file
DATABASE_URL=postgresql://postgres:password@localhost:5432/legal_assist
```

### Issue: "LLM service unavailable"
**Solution:** Verify Groq API key in .env
```bash
GROQ_API_KEY=your-api-key-here
LLM_MODEL=llama-3.1-8b-instant
```

### Issue: "No documents found" in search
**Solution:** 
1. Verify documents exist: `GET /documents/`
2. Check embeddings were generated
3. Lower `min_similarity` threshold (try 0.0)

### Issue: Slow first request
**Solution:** This is normal - embedding model loads on first use (~2-3 seconds)

---

## Advanced Testing

### Test with cURL
```bash
# Health check
curl http://localhost:8000/health

# RAG query
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Section 302?",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "top_k": 5
  }'
```

### Test with Python
```python
import requests

# RAG query
response = requests.post(
    "http://localhost:8000/rag/query",
    json={
        "query": "What is the punishment for murder?",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "top_k": 5
    }
)
print(response.json())
```

### Load Testing
```bash
# Install Apache Bench
# Test 100 requests with 10 concurrent
ab -n 100 -c 10 -T application/json \
   -p query.json \
   http://localhost:8000/rag/query
```

---

## Sample Test Data

### Sample Categories
```json
[
  {
    "title": "Indian Penal Code",
    "description": "Criminal law sections",
    "is_active": true
  },
  {
    "title": "Insurance Law",
    "description": "Insurance policies and regulations",
    "is_active": true
  },
  {
    "title": "Contract Law",
    "description": "Contract provisions and clauses",
    "is_active": true
  }
]
```

### Sample Documents
```json
[
  {
    "title": "Section 302 IPC - Murder",
    "content": "Section 302 of the Indian Penal Code deals with punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
    "tags": ["ipc", "criminal", "murder"]
  },
  {
    "title": "Section 420 IPC - Cheating",
    "content": "Section 420 of the Indian Penal Code deals with cheating and dishonestly inducing delivery of property. Punishment includes imprisonment up to seven years and fine.",
    "tags": ["ipc", "criminal", "fraud"]
  }
]
```

### Sample Queries
```json
[
  "What is the punishment for murder under IPC?",
  "Explain Section 420 of IPC",
  "What are the penalties for cheating?",
  "Tell me about insurance claim settlement procedures",
  "What is the difference between murder and culpable homicide?"
]
```

---

## Next Steps

1. ✅ Import `api_documentation.yaml` into Postman
2. ✅ Create test environment with variables
3. ✅ Run the Quick Test Sequence
4. ✅ Test all CRUD operations
5. ✅ Test RAG pipeline with various queries
6. ✅ Monitor performance and logs
7. ✅ Test error scenarios (invalid UUIDs, missing fields, etc.)

---

## Support

For issues or questions:
- Check backend logs in terminal
- Review `api_documentation.yaml` for detailed schemas
- Visit Swagger UI at `http://localhost:8000/docs`
- Check database with PostgreSQL client

Happy Testing! 🚀
