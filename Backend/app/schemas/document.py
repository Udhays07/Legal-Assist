"""
Pydantic schemas for Document operations.

Defines create/update/read schemas for the `Document` core entity. Schemas are
kept independent from ORM models so API contracts remain stable as internal
models evolve. Pydantic v2 ``ConfigDict(from_attributes=True)`` is set to allow
returning SQLAlchemy model instances directly from FastAPI endpoints.
"""

from __future__ import annotations

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class DocumentBase(BaseModel):
    """Shared document fields for create and update operations."""

    category_id: UUID = Field(..., description="ID of the category this document belongs to")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Main textual content of the document")
    tags: Optional[List[str]] = Field(None, description="Optional list of tags for search")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional structured metadata")
    status: Optional[str] = Field("published", description="Document status")

    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(DocumentBase):
    """Schema used when creating a new document."""

    created_by: Optional[UUID] = Field(None, description="User ID who created the document")


class DocumentUpdate(BaseModel):
    """Schema for partial updates to a document (PATCH-like)."""

    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DocumentRead(DocumentBase):
    """Schema returned by the API for Document resources."""

    id: UUID
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class DocumentListItem(DocumentRead):
    """Slim variant for list endpoints if needed (inherits DocumentRead).

    Keep this separate so you can later add list-specific fields (excerpts,
    search highlights) without changing the main `DocumentRead` contract.
    """

    pass
