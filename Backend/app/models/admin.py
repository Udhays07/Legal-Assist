"""
SQLAlchemy ORM models for Legal Assistant core entities: Role, User, Category, Document, and DocumentEmbedding.

- Role: System roles, seeded at DB initialization, not editable.
- User: Application users, supports soft delete.
- Category: Document categories, supports soft delete and enable/disable.
- Document: Core knowledge entity, supports metadata, tags, soft delete.
- DocumentEmbedding: (Optional) For future vector search support.

All models use UUID primary keys and timestamp fields for audit and soft delete logic.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, ARRAY, Index, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid
from ..core.database import Base

class Role(Base):
    """
    Role model for user authorization.
    - Only 'id' and 'name' fields.
    - Seeded at DB initialization, not editable.
    """
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    users = relationship("User", back_populates="role")

class User(Base):
    """
    User model with soft delete and audit fields.
    """
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    role = relationship("Role", back_populates="users")
    documents = relationship("Document", back_populates="creator")

class Category(Base):
    """
    Category model for document organization.
    Supports soft delete and enable/disable.
    """
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    documents = relationship("Document", back_populates="category")

class Document(Base):
    """
    Document model as the core knowledge entity.
    Supports metadata, tags, status, and soft delete.
    """
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    # 'metadata' is a reserved attribute name on Declarative base (Base.metadata).
    # Use a different attribute name but keep the column name as 'metadata' in the DB.
    metadata_json = Column('metadata', JSONB, nullable=True)
    status = Column(String, server_default="published", nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    category = relationship("Category", back_populates="documents")
    creator = relationship("User", back_populates="documents")
    embedding = relationship("DocumentEmbedding", uselist=False, back_populates="document")
    __table_args__ = (
        Index("ix_documents_tags", "tags", postgresql_using="gin"),
        Index(
            "ix_documents_fts",
            func.to_tsvector("english", title + " " + content),
            postgresql_using="gin",
        ),
    )

class DocumentEmbedding(Base):
    """
    Document embedding for vector search support using pgvector.
    Embedding should be updated on document update and removed on soft delete.
    Uses all-mpnet-base-v2 model (768 dimensions).
    """
    __tablename__ = "document_embeddings"
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    embedding = Column(Vector(768), nullable=False)  # 768 dimensions for all-mpnet-base-v2
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    document = relationship("Document", back_populates="embedding")