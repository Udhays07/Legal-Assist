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

import json
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.admin import Document
from app.schemas.document import DocumentRead, DocumentUpdate
from app.utils.file_extractor import extract_text, UnsupportedFileTypeError, ContentTooShortError, FileExtractionError
from app.services.embedding_service import create_or_update_embedding, delete_embedding

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    category_id: UUID = Form(...),
    title: str = Form(...),
    content: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),  # Expects JSON string like '["a", "b"]'
    doc_status: str = Form("published", alias="status"),
    created_by: Optional[UUID] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Create a new document.
    
    Accepts content either as a plain string in the 'content' field 
    OR as an uploaded file in the 'file' field. If a file is provided, 
    its text content is extracted and validated.
    """
    final_content = content

    # 1. If file is provided, extract its content
    if file:
        try:
            file_bytes = file.file.read()
            final_content = extract_text(file.filename, file_bytes)
        except (UnsupportedFileTypeError, ContentTooShortError, FileExtractionError) as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error processing file: {str(e)}"
            )
    
    # 2. Check if we have any content at all
    if not final_content or not final_content.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No content found. Please provide text content or upload a file."
        )

    # 3. Parse tags if provided as JSON string
    parsed_tags = None
    if tags:
        try:
            parsed_tags = json.loads(tags)
            if not isinstance(parsed_tags, list):
                parsed_tags = [str(parsed_tags)]
        except json.JSONDecodeError:
            parsed_tags = [tags]

    # 4. Create and persist document
    doc = Document(
        category_id=category_id,
        title=title,
        content=final_content,
        tags=parsed_tags,
        metadata_json=None,  # Not currently exposure in form
        status=doc_status,
        created_by=created_by,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # 5. Generate and store embedding for the document content
    try:
        create_or_update_embedding(db, doc.id, final_content)
    except Exception as e:
        # Log the error but don't fail the document creation
        # The embedding can be regenerated later if needed
        print(f"Warning: Failed to generate embedding for document {doc.id}: {str(e)}")
    
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
    
    content_updated = False
    
    if payload.title is not None:
        doc.title = payload.title
    if payload.content is not None:
        doc.content = payload.content
        content_updated = True
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
    
    # Regenerate embedding if content was updated
    if content_updated:
        try:
            create_or_update_embedding(db, doc.id, doc.content)
        except Exception as e:
            # Log the error but don't fail the document update
            print(f"Warning: Failed to update embedding for document {doc.id}: {str(e)}")
    
    return doc


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Soft-delete a document by setting `deleted_at` and remove its embedding."""
    doc = db.query(Document).filter(Document.id == document_id, Document.deleted_at == None).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.deleted_at = datetime.utcnow()
    db.add(doc)
    db.commit()
    
    # Delete the associated embedding
    try:
        delete_embedding(db, doc.id)
    except Exception as e:
        # Log the error but don't fail the document deletion
        print(f"Warning: Failed to delete embedding for document {doc.id}: {str(e)}")
    
    return None