"""
Application constants and configuration values.

This module centralizes all constant values used across the application
to ensure consistency and easy maintenance.
"""

# Embedding Model Configuration
MODEL_NAME = "intfloat/e5-base-v2"
EMBEDDING_DIMENSION = 768

# Model Information
MODEL_INFO = {
    "name": MODEL_NAME,
    "dimension": EMBEDDING_DIMENSION,
    "description": "E5-base-v2 model for high-quality semantic embeddings",
    "license": "MIT",
    "size_mb": 411,
    "requires_prefix": True,
    "query_prefix": "query: ",
    "passage_prefix": "passage: ",
}
