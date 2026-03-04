# RAG Implementation Plan

## ✅ Completed Steps

### 1. Similarity Search Service ✅
**File**: `app/services/search_service.py`

Features:
- Semantic search using e5-base-v2 embeddings
- Configurable top-k results
- Filtering by category, status, min_similarity
- Find similar documents
- Search within categories

### 2. Database Schema for Chat ✅
**File**: `app/models/chat.py`

Tables created:
- **conversations**: Chat sessions
- **messages**: User queries and assistant responses
- **user_activities**: Track user interactions
- **search_history**: Search analytics

**File**: `app/schemas/chat.py`
- Pydantic schemas for API requests/responses

## 🔨 Next Steps

### 3. RAG API Endpoint
Create: `app/api/rag.py`

Endpoints needed:
```python
POST /rag/query          # Main RAG endpoint
GET  /rag/conversations  # List user conversations
GET  /rag/conversations/{id}  # Get conversation with messages
POST /rag/feedback       # Submit message feedback
GET  /search             # Semantic search endpoint
```

### 4. Choose Open Source LLM

**Options:**

#### A. Ollama (Recommended - Free, Local)
- **Models**: Llama 3, Mistral, Phi-3
- **Pros**: Free, runs locally, no API costs, privacy
- **Cons**: Requires GPU for good performance
- **Setup**: `ollama pull llama3`

#### B. Hugging Face Models
- **Models**: Llama 2, Mistral, Falcon
- **Pros**: Free, many options
- **Cons**: Need to host yourself or use API

#### C. GPT4All
- **Models**: Various open source models
- **Pros**: Easy to use, runs locally
- **Cons**: Slower than Ollama

**Recommendation**: **Ollama with Llama 3** (8B or 70B)
- Best quality for legal documents
- Free and runs locally
- Easy integration
- Good speed with GPU

### 5. LLM Integration
Create: `app/services/llm_service.py`

Features needed:
- Connect to chosen LLM
- Format prompts with context
- Handle streaming responses
- Error handling and retries
- Token counting

## Implementation Order

### Phase 1: Search API (Week 1)
1. Create search endpoint
2. Test similarity search
3. Add search history tracking

### Phase 2: RAG Service (Week 2)
1. Choose and setup LLM (Ollama recommended)
2. Create RAG service
3. Implement prompt engineering
4. Test with sample queries

### Phase 3: Chat API (Week 3)
1. Create conversation management
2. Create RAG query endpoint
3. Add message feedback
4. Test end-to-end flow

### Phase 4: Polish (Week 4)
1. Add streaming responses
2. Optimize performance
3. Add analytics
4. Documentation

## Database Migration Needed

Create migration for new tables:

```bash
# Generate migration
alembic revision --autogenerate -m "add chat and rag tables"

# Apply migration
alembic upgrade head
```

## Environment Variables to Add

```env
# LLM Configuration
LLM_PROVIDER=ollama  # or openai, anthropic
LLM_MODEL=llama3
LLM_BASE_URL=http://localhost:11434  # For Ollama
LLM_API_KEY=  # If using paid API

# RAG Configuration
RAG_TOP_K=5
RAG_MIN_SIMILARITY=0.3
RAG_MAX_CONTEXT_LENGTH=4000
```

## System Prompt Template

```python
SYSTEM_PROMPT = """
You are a legal assistant AI helping users understand legal documents.

Context from relevant documents:
{context}

Instructions:
- Answer based ONLY on the provided context
- If the answer is not in the context, say "I don't have enough information"
- Cite specific documents when possible
- Be precise and professional
- Use legal terminology appropriately

User Question: {question}

Answer:
"""
```

## Testing Strategy

1. **Unit Tests**
   - Test search service
   - Test embedding generation
   - Test LLM integration

2. **Integration Tests**
   - Test full RAG pipeline
   - Test conversation flow
   - Test error handling

3. **Performance Tests**
   - Search latency (<100ms)
   - RAG response time (<3s)
   - Concurrent users

## Success Metrics

- Search accuracy: >80% relevant results
- RAG response time: <3 seconds
- User satisfaction: >4/5 rating
- System uptime: >99%

## Next Immediate Actions

1. **Run database migration**
   ```bash
   alembic revision --autogenerate -m "add chat tables"
   alembic upgrade head
   ```

2. **Install Ollama** (if choosing local LLM)
   ```bash
   # Download from https://ollama.ai
   ollama pull llama3
   ```

3. **Create RAG service**
   - Implement LLM integration
   - Create prompt templates
   - Add response generation

4. **Create RAG API**
   - Add endpoints
   - Test with Postman/curl
   - Integrate with frontend

---

**Current Status**: Steps 1 & 2 Complete ✅  
**Next**: Database migration → LLM setup → RAG service  
**Timeline**: 2-4 weeks for full implementation
