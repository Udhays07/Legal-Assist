# Legal Assistant Backend API Documentation

Complete API documentation and testing resources for the Legal Assistant backend system.

## 📚 Documentation Files

### 1. **api_documentation.yaml** (OpenAPI 3.0 Spec)
Complete OpenAPI specification with all endpoints, schemas, and examples.

**Use for:**
- Importing into API tools (Postman, Insomnia, etc.)
- Generating client SDKs
- API contract validation
- Team collaboration

### 2. **Legal_Assistant_API.postman_collection.json**
Ready-to-use Postman collection with pre-configured requests.

**Features:**
- All endpoints pre-configured
- Collection variables for easy testing
- Auto-save IDs (category_id, document_id, conversation_id)
- Sample queries included

### 3. **API_TESTING_GUIDE.md**
Step-by-step testing guide with examples and troubleshooting.

**Includes:**
- Quick test sequences
- Common scenarios
- cURL examples
- Python examples
- Troubleshooting tips

---

## 🚀 Quick Start

### Option 1: Use Swagger UI (Recommended for Quick Testing)
1. Start the backend server:
   ```bash
   cd Backend
   python -m uvicorn app.main:app --reload
   ```

2. Open your browser:
   ```
   http://localhost:8000/docs
   ```

3. Click "Try it out" on any endpoint and test directly!

### Option 2: Import into Postman
1. Open Postman
2. Click "Import" → "Upload Files"
3. Select `Legal_Assistant_API.postman_collection.json`
4. All requests are ready to use!

### Option 3: Use OpenAPI Spec
1. Import `api_documentation.yaml` into:
   - Postman
   - Insomnia
   - Swagger Editor
   - Any OpenAPI-compatible tool

---

## 📖 Available Documentation Endpoints

Once the server is running:

| Endpoint | Description |
|----------|-------------|
| `/docs` | Interactive Swagger UI |
| `/redoc` | Beautiful ReDoc documentation |
| `/openapi.json` | OpenAPI spec in JSON format |

---

## 🎯 API Overview

### RAG System Endpoints
- `POST /rag/query` - Ask questions and get AI-generated answers
- `POST /rag/search` - Semantic search without AI response
- `GET /rag/conversations` - List user conversations
- `GET /rag/conversations/{id}` - Get conversation history
- `POST /rag/feedback` - Submit feedback on responses
- `GET /rag/health` - Check RAG system health

### Document Management
- `POST /documents/` - Create document (text or file upload)
- `GET /documents/` - List all documents
- `GET /documents/{id}` - Get single document
- `PUT /documents/{id}` - Update document
- `DELETE /documents/{id}` - Delete document

### Category Management
- `POST /categories/` - Create category
- `GET /categories/` - List categories
- `GET /categories/{id}` - Get single category
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

### Health Checks
- `GET /health` - Application health
- `GET /rag/health` - RAG system health

---

## 🧪 Testing Workflow

### 1. Basic Setup
```bash
# Start server
cd Backend
python -m uvicorn app.main:app --reload

# Check health
curl http://localhost:8000/health
```

### 2. Create Test Data
```bash
# Create category
curl -X POST http://localhost:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Indian Penal Code",
    "description": "IPC sections",
    "is_active": true
  }'

# Create document (save category_id from above)
curl -X POST http://localhost:8000/documents/ \
  -F "category_id=YOUR_CATEGORY_ID" \
  -F "title=Section 302 IPC" \
  -F "content=Section 302 deals with punishment for murder..." \
  -F "tags=[\"ipc\", \"criminal\"]" \
  -F "status=published"
```

### 3. Test RAG System
```bash
# Ask a question
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the punishment for murder?",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "top_k": 5,
    "include_sources": true
  }'
```

---

## 🔑 Key Features

### Automatic Embeddings
Documents are automatically converted to embeddings (768-dimensional vectors) using the E5-base-v2 model when created or updated.

### Semantic Search
Search uses cosine similarity on vector embeddings to find relevant documents, not just keyword matching.

### Conversation History
All RAG queries are saved with conversation context, allowing follow-up questions.

### Source Citations
AI responses include references to source documents with similarity scores.

### Performance Tracking
All responses include `processing_time_ms` for monitoring.

---

## 📊 Response Examples

### RAG Query Response
```json
{
  "answer": "Section 302 of the Indian Penal Code deals with...",
  "sources": [
    {
      "id": "uuid-here",
      "title": "Section 302 IPC",
      "content": "Full content...",
      "similarity": 0.8743,
      "category_id": "uuid-here"
    }
  ],
  "conversation_id": "uuid-here",
  "message_id": "uuid-here",
  "processing_time_ms": 507,
  "model_used": "llama-3.1-8b-instant"
}
```

### Search Response
```json
{
  "query": "insurance claims",
  "results": [
    {
      "id": "uuid-here",
      "title": "Insurance Claims Guide",
      "content": "Preview...",
      "similarity": 0.85,
      "tags": ["insurance", "claims"]
    }
  ],
  "total_results": 5,
  "processing_time_ms": 150
}
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/legal_assist

# LLM (Groq)
GROQ_API_KEY=your-api-key-here
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# RAG Settings
RAG_TOP_K=5
RAG_MIN_SIMILARITY=0.1
RAG_MAX_CONTEXT_LENGTH=4000

# Embeddings
EMBEDDING_MODEL=intfloat/e5-base-v2
EMBEDDING_DIMENSION=768
```

---

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Activate virtual environment
cd Backend
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Issue: "Database connection failed"
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Test connection:
psql -U postgres -d legal_assist
```

### Issue: "LLM service unavailable"
```bash
# Check Groq API key in .env
# Verify GROQ_API_KEY is valid
# Check /rag/health endpoint
```

### Issue: Slow first request
This is normal - the embedding model loads on first use (~2-3 seconds). Subsequent requests are fast.

---

## 📝 Testing Checklist

- [ ] Health checks pass (`/health`, `/rag/health`)
- [ ] Can create categories
- [ ] Can create documents (text and file upload)
- [ ] Documents appear in list
- [ ] Can update documents
- [ ] RAG query returns answer with sources
- [ ] Follow-up questions work in same conversation
- [ ] Semantic search finds relevant documents
- [ ] Conversation history is saved
- [ ] Feedback submission works
- [ ] Can delete documents and categories

---

## 🤝 Collaboration

### For Team Members
1. Import `Legal_Assistant_API.postman_collection.json` into Postman
2. Set `base_url` variable to your server URL
3. Run through the "Sample Test Queries" folder
4. Check `API_TESTING_GUIDE.md` for detailed scenarios

### For Frontend Developers
1. Review `api_documentation.yaml` for complete API contract
2. Use `/docs` endpoint for interactive testing
3. All responses follow consistent schema patterns
4. UUIDs are used for all resource identifiers

### For QA/Testing
1. Use Postman collection for manual testing
2. Check `API_TESTING_GUIDE.md` for test scenarios
3. Monitor `processing_time_ms` for performance
4. Test error scenarios (invalid UUIDs, missing fields)

---

## 📚 Additional Resources

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **Testing Guide**: `API_TESTING_GUIDE.md`
- **Main README**: `README.md`

---

## 🎉 Ready to Test!

1. Start the server: `python -m uvicorn app.main:app --reload`
2. Open Swagger UI: http://localhost:8000/docs
3. Try the "RAG Query" endpoint with: "What is Section 302 of IPC?"
4. Explore the interactive documentation!

Happy Testing! 🚀
