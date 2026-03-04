# Using Groq API (Fast & Free Alternative)

Groq provides free, ultra-fast LLM inference. It's much faster than running Ollama on CPU.

## Setup Steps

### 1. Get Groq API Key
1. Go to https://console.groq.com
2. Sign up for free account
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### 2. Install Groq SDK
```bash
pip install groq
```

### 3. Update .env file
```env
# Change from Ollama to Groq
LLM_PROVIDER=groq
LLM_MODEL=llama3-70b-8192
GROQ_API_KEY=gsk_your_api_key_here
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

### 4. Update llm_service.py

Add Groq support to your LLM service. I'll create an updated version.

## Available Models on Groq

- `llama3-70b-8192` - Llama 3 70B (recommended, very fast)
- `llama3-8b-8192` - Llama 3 8B (faster, smaller)
- `mixtral-8x7b-32768` - Mixtral 8x7B
- `gemma-7b-it` - Google Gemma 7B

## Advantages

✅ **Much faster** than CPU Ollama (responses in 1-2 seconds)
✅ **Free tier** with generous limits
✅ **No GPU needed** on your machine
✅ **No Colab setup** required
✅ **Reliable** - no timeouts

## Rate Limits (Free Tier)

- 30 requests per minute
- 14,400 requests per day
- More than enough for development and testing
