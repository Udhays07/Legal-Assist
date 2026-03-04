"""
LLM service supporting both Ollama and Groq.

This service handles interaction with LLM APIs to generate
responses for the RAG system.

Supported Providers:
- Ollama (local, requires GPU/CPU)
- Groq (cloud, fast and free)

Usage:
    Set LLM_PROVIDER in .env to either "ollama" or "groq"
"""

import logging
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

from app.core.constants import (
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_LLM_MAX_TOKENS,
    DEFAULT_LLM_MODEL,
)

load_dotenv()

logger = logging.getLogger(__name__)


class GroqLLMService:
    """Service for interacting with Groq API."""
    
    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_LLM_MODEL,
        temperature: float = DEFAULT_LLM_TEMPERATURE,
        max_tokens: int = DEFAULT_LLM_MAX_TOKENS
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Import groq here to avoid dependency if not using it
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("Groq SDK not installed. Run: pip install groq")
    
    def check_health(self) -> bool:
        """Check if Groq API is accessible."""
        try:
            # Try to list models as a health check
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Groq health check failed: {str(e)}")
            return False
    
    def list_models(self) -> List[str]:
        """List available models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            return []
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate a response using Groq.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Override default max tokens
            temperature: Override default temperature
        
        Returns:
            Generated response text
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Groq generation failed: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """Approximate token count (4 chars ≈ 1 token)."""
        return len(text) // 4


def get_llm_service():
    """
    Factory function to get the appropriate LLM service based on configuration.
    
    Returns:
        LLMService instance (Ollama or Groq)
    """
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))
        
        logger.info(f"Using Groq LLM service with model: {model}")
        return GroqLLMService(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    elif provider == "ollama":
        # Import the existing Ollama service
        from app.services.llm_service import LLMService
        
        base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434")
        model = os.getenv("LLM_MODEL", "llama3")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))
        
        logger.info(f"Using Ollama LLM service at {base_url} with model: {model}")
        return LLMService(
            base_url=base_url,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Use 'ollama' or 'groq'")