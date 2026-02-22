"""
Document API router.

Provides endpoints to create, list, retrieve, update and soft-delete documents.

Routes:
 - POST /documents
 - GET  /documents
 - GET  /documents/{document_id}
 - PUT  /documents/{document_id}
 - DELETE /documents/{document_id}

Supports listing by category via query parameter `category_id` and basic
filters for status and tags.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.admin import Document
from app.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    """Create a new document."""
    doc = Document(
        category_id=payload.category_id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        metadata_json=payload.metadata,
        status=payload.status,
        created_by=payload.created_by,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/", response_model=List[DocumentRead])
def list_documents(category_id: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    """List documents with optional filters."""
    q = db.query(Document).filter(Document.deleted_at == None)
    if category_id:
        q = q.filter(Document.category_id == category_id)
    if status:
        q = q.filter(Document.status == status)
    return q.order_by(Document.created_at.desc()).all()


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: str, db: Session = Depends(get_db)):
    """Retrieve a single document by id."""
    doc = db.query(Document).filter(Document.id == document_id, Document.deleted_at == None).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.put("/{document_id}", response_model=DocumentRead)
def update_document(document_id: str, payload: DocumentUpdate, db: Session = Depends(get_db)):
    """Update a document partially."""
    doc = db.query(Document).filter(Document.id == document_id, Document.deleted_at == None).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if payload.title is not None:
        doc.title = payload.title
    if payload.content is not None:
        doc.content = payload.content
    if payload.tags is not None:
        doc.tags = payload.tags
    if payload.metadata is not None:
        doc.metadata_json = payload.metadata
    if payload.status is not None:
        doc.status = payload.status
    doc.updated_at = datetime.utcnow()
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Soft-delete a document by setting `deleted_at`."""
    doc = db.query(Document).filter(Document.id == document_id, Document.deleted_at == None).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.deleted_at = datetime.utcnow()
    db.add(doc)
    db.commit()
    return None
