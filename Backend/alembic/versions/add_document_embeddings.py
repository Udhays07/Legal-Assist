"""add document embeddings table with pgvector

Revision ID: add_embeddings_001
Revises: d911513ed61e
Create Date: 2026-03-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = 'add_embeddings_001'
down_revision: Union[str, None] = 'd911513ed61e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create document_embeddings table
    op.create_table(
        'document_embeddings',
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('embedding', Vector(768), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], name=op.f('fk_document_embeddings_document_id_documents')),
        sa.PrimaryKeyConstraint('document_id', name=op.f('pk_document_embeddings'))
    )
    
    # Create index for vector similarity search (using cosine distance)
    op.execute(
        'CREATE INDEX idx_document_embeddings_vector ON document_embeddings '
        'USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)'
    )


def downgrade() -> None:
    # Drop the index first
    op.execute('DROP INDEX IF EXISTS idx_document_embeddings_vector')
    
    # Drop the table
    op.drop_table('document_embeddings')
    
    # Optionally drop the extension (commented out to avoid affecting other tables)
    # op.execute('DROP EXTENSION IF EXISTS vector')
