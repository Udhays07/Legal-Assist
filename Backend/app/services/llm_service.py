"""
LLM service for generating responses using Ollama.

This service handles interaction with the Ollama API to generate
responses for the RAG system using Llama 3 or other models.

Key Features:
- Ollama API integration
- Prompt formatting with context
- Streaming support
- Error handling and retries
- Token counting (approximate)

System Dependencies:
- Depends on: Ollama running locally (default: http://localhost:11434)
- Depended by: rag_service for response generation
"""

import logging
import requests
import json
from typing import Optional, List, Dict, Any, Generator
import time

logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000


class LLMService:
    """Service for interacting with Ollama LLM."""
    
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS
    ):
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def check_health(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            bool: True if Ollama is healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False
    
    def list_models(self) -> List[str]:
        """
        List available models in Ollama.
        
        Returns:
            List[str]: List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            return []
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            stream: Whether to stream the response
        
        Returns:
            str: Generated response
        
        Raises:
            Exception: If generation fails
        """
        try:
            start_time = time.time()
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make request
            logger.info(f"Generating response with {self.model}")
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
            # Parse response
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        full_response += data.get("response", "")
                        if data.get("done", False):
                            break
                result = full_response
            else:
                # Handle non-streaming response
                data = response.json()
                result = data.get("response", "")
            
            elapsed_time = (time.time() - start_time) * 1000
            logger.info(f"Response generated in {elapsed_time:.0f}ms")
            
            return result.strip()
            
        except requests.exceptions.Timeout:
            logger.error("LLM request timed out")
            raise Exception("Request timed out. Please try again.")
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            raise
    
    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
        
        Yields:
            str: Response chunks
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    if chunk:
                        yield chunk
                    if data.get("done", False):
                        break
                        
        except Exception as e:
            logger.error(f"Streaming generation failed: {str(e)}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """
        Approximate token count for text.
        
        Args:
            text: Text to count tokens for
        
        Returns:
            int: Approximate token count
        """
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4


# Global LLM service instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get or initialize the LLM service (singleton pattern).
    
    Returns:
        LLMService: The LLM service instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
        logger.info(f"LLM service initialized with model: {_llm_service.model}")
    return _llm_service


def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    **kwargs
) -> str:
    """
    Convenience function to generate a response.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        **kwargs: Additional arguments for generation
    
    Returns:
        str: Generated response
    """
    llm = get_llm_service()
    return llm.generate(prompt, system_prompt, **kwargs)