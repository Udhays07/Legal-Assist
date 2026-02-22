"""
Pydantic schemas for Category operations.

This module defines request and response schemas used by the API endpoints
that manage `Category` entities. Schemas are intentionally small and focused
to follow separation-of-concerns between models (ORM) and API contracts.

All schemas are compatible with Pydantic v2 and configured to load from
ORM objects using `model_config = ConfigDict(from_attributes=True)` so
SQLAlchemy model instances can be returned directly in FastAPI responses.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CategoryBase(BaseModel):
    """Shared fields for create/update operations."""

    title: str = Field(..., description="Unique title for the category")
    description: Optional[str] = Field(None, description="Optional description")
    is_active: Optional[bool] = Field(True, description="Whether the category is enabled")

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    """Schema used when creating a new Category."""


class CategoryUpdate(BaseModel):
    """Fields allowed when updating a Category. All fields are optional."""

    title: Optional[str] = Field(None, description="New title (must remain unique)")
    description: Optional[str] = Field(None, description="New description")
    is_active: Optional[bool] = Field(None, description="Enable or disable the category")

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(CategoryBase):
    """Schema returned by the API for Category resources."""

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = Field(None, description="Soft-delete timestamp if removed")

    model_config = ConfigDict(from_attributes=True)
