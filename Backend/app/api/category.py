"""
Category API router.

Provides endpoints to create, list, retrieve, update and soft-delete categories.
Soft-deleting a category will also soft-delete associated documents.

Routes:
 - POST /categories
 - GET  /categories
 - GET  /categories/{category_id}
 - PUT  /categories/{category_id}
 - DELETE /categories/{category_id}

This module uses SQLAlchemy sessions from `app.core.database.get_db` and
Pydantic schemas from `app.schemas.category` for request/response validation.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.admin import Category, Document
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    exists = db.query(Category).filter(Category.title == payload.title, Category.deleted_at == None).first()
    if exists:
        raise HTTPException(status_code=400, detail="Category with this title already exists")
    category = Category(title=payload.title, description=payload.description, is_active=payload.is_active)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=List[CategoryRead])
def list_categories(include_inactive: bool = False, db: Session = Depends(get_db)):
    """Return all categories; by default only active, non-deleted categories."""
    q = db.query(Category).filter(Category.deleted_at == None)
    if not include_inactive:
        q = q.filter(Category.is_active == True)
    return q.order_by(Category.title).all()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: str, db: Session = Depends(get_db)):
    """Retrieve a single category by id."""
    category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category's fields."""
    category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if payload.title is not None:
        # ensure uniqueness
        other = db.query(Category).filter(Category.title == payload.title, Category.id != category_id, Category.deleted_at == None).first()
        if other:
            raise HTTPException(status_code=400, detail="Category title already in use")
        category.title = payload.title
    if payload.description is not None:
        category.description = payload.description
    if payload.is_active is not None:
        category.is_active = payload.is_active
    category.updated_at = datetime.utcnow()
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """Soft-delete a category and its documents by setting `deleted_at`."""
    category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    ts = datetime.utcnow()
    category.deleted_at = ts
    db.add(category)
    # soft delete associated documents
    db.query(Document).filter(Document.category_id == category.id, Document.deleted_at == None).update({Document.deleted_at: ts})
    db.commit()
    return None
