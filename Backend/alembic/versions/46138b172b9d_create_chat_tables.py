"""create_chat_tables

Revision ID: 46138b172b9d
Revises: 6e62230bcbee
Create Date: 2026-03-04 18:12:18.918020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46138b172b9d'
down_revision: Union[str, None] = '6e62230bcbee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_conversations_user'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'])
    op.create_index('idx_conversations_deleted_at', 'conversations', ['deleted_at'])
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('retrieved_documents', sa.JSON(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('model_used', sa.String(), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='chk_messages_role'),
        sa.CheckConstraint('rating IS NULL OR (rating >= 1 AND rating <= 5)', name='chk_messages_rating'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='fk_messages_conversation', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])
    op.create_index('idx_messages_role', 'messages', ['role'])
    op.create_index('idx_messages_rating', 'messages', ['rating'], postgresql_where=sa.text('rating IS NOT NULL'))
    
    # Create search_history table
    op.create_table(
        'search_history',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('results_count', sa.Integer(), nullable=False),
        sa.Column('top_result_id', sa.UUID(), nullable=True),
        sa.Column('top_similarity', sa.Float(), nullable=True),
        sa.Column('filters', sa.JSON(), nullable=True),
        sa.Column('clicked_result_id', sa.UUID(), nullable=True),
        sa.Column('clicked_position', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint('clicked_position IS NULL OR clicked_position > 0', name='chk_search_history_clicked_position'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_search_history_user'),
        sa.ForeignKeyConstraint(['top_result_id'], ['documents.id'], name='fk_search_history_top_result'),
        sa.ForeignKeyConstraint(['clicked_result_id'], ['documents.id'], name='fk_search_history_clicked_result'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_search_history_user_id', 'search_history', ['user_id'], postgresql_where=sa.text('user_id IS NOT NULL'))
    op.create_index('idx_search_history_created_at', 'search_history', ['created_at'])
    op.create_index('idx_search_history_top_result_id', 'search_history', ['top_result_id'], postgresql_where=sa.text('top_result_id IS NOT NULL'))
    
    # Create user_activities table
    op.create_table(
        'user_activities',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('activity_type', sa.String(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('document_id', sa.UUID(), nullable=True),
        sa.Column('conversation_id', sa.UUID(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_activities_user'),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], name='fk_user_activities_document'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='fk_user_activities_conversation'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_activities_user_id', 'user_activities', ['user_id'])
    op.create_index('idx_user_activities_activity_type', 'user_activities', ['activity_type'])
    op.create_index('idx_user_activities_created_at', 'user_activities', ['created_at'])
    op.create_index('idx_user_activities_document_id', 'user_activities', ['document_id'], postgresql_where=sa.text('document_id IS NOT NULL'))
    op.create_index('idx_user_activities_conversation_id', 'user_activities', ['conversation_id'], postgresql_where=sa.text('conversation_id IS NOT NULL'))


def downgrade() -> None:
    op.drop_table('user_activities')
    op.drop_table('search_history')
    op.drop_table('messages')
    op.drop_table('conversations')
