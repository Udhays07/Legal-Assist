"""
Application constants and configuration values.

This module centralizes all constant values used across the application
to ensure consistency and easy maintenance.
"""

# Embedding Model Configuration
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_DIMENSION = 768

# Model Information
MODEL_INFO = {
    "name": MODEL_NAME,
    "dimension": EMBEDDING_DIMENSION,
    "description": "All-mpnet-base-v2 model for semantic embeddings",
    "license": "Apache 2.0",
    "size_mb": 420,
}
