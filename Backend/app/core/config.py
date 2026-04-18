"""
Application configuration management and environment settings.

Centralizes all configuration parameters, environment variables,
and application settings using Pydantic BaseSettings for type-safe
validation with defaults for local development.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env file.
    All fields have sensible defaults for local development.
    """

    # Database
    DATABASE_URL: str = "postgresql://postgres:sql@localhost:5432/legal_assist"

    # JWT / Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Debug
    DEBUG: bool = True

    # RAG Configuration
    RAG_TOP_K: int = 5
    RAG_MIN_SIMILARITY: float = 0.1
    RAG_MAX_CONTEXT_LENGTH: int = 4000

    # Embedding Model
    EMBEDDING_MODEL: str = "intfloat/e5-base-v2"
    EMBEDDING_DIMENSION: int = 768

    # LLM Configuration
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.1-8b-instant"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()


# Module-level singleton for convenient import
settings = get_settings()
