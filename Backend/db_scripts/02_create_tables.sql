-- ============================================================
-- Legal Assistant - Table Creation Script
-- ============================================================
-- Creates all tables for the Legal Assistant application
-- Run this after 01_create_database.sql
-- ============================================================

\c legal_assist;

-- ============================================================
-- Core Tables
-- ============================================================

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL UNIQUE,
    CONSTRAINT roles_name_check CHECK (name IN ('admin', 'user'))
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT users_id_unique UNIQUE (id)
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT categories_id_unique UNIQUE (id)
);

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID NOT NULL REFERENCES categories(id),
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    tags VARCHAR[],
    metadata JSONB,
    status VARCHAR NOT NULL DEFAULT 'published',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT documents_id_unique UNIQUE (id),
    CONSTRAINT documents_status_check CHECK (status IN ('published', 'draft', 'archived'))
);

-- Create GIN index for tags array
CREATE INDEX IF NOT EXISTS ix_documents_tags ON documents USING GIN (tags);

-- Document embeddings table (for vector search)
CREATE TABLE IF NOT EXISTS document_embeddings (
    document_id UUID PRIMARY KEY REFERENCES documents(id) ON DELETE CASCADE,
    embedding vector(768) NOT NULL,  -- 768 dimensions for e5-base-v2 model
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS document_embeddings_embedding_idx 
ON document_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- ============================================================
-- Chat and RAG Tables
-- ============================================================

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT conversations_id_unique UNIQUE (id)
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR NOT NULL,
    content TEXT NOT NULL,
    retrieved_documents JSONB,
    processing_time_ms INTEGER,
    model_used VARCHAR,
    tokens_used INTEGER,
    rating INTEGER,
    feedback TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT messages_id_unique UNIQUE (id),
    CONSTRAINT messages_role_check CHECK (role IN ('user', 'assistant')),
    CONSTRAINT messages_rating_check CHECK (rating IS NULL OR (rating >= 1 AND rating <= 5))
);

-- User activities table (for analytics)
CREATE TABLE IF NOT EXISTS user_activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    activity_type VARCHAR NOT NULL,
    details JSONB,
    document_id UUID REFERENCES documents(id),
    conversation_id UUID REFERENCES conversations(id),
    ip_address VARCHAR,
    user_agent VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT user_activities_id_unique UNIQUE (id)
);

-- Search history table
CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    query TEXT NOT NULL,
    results_count INTEGER NOT NULL,
    top_result_id UUID REFERENCES documents(id),
    top_similarity FLOAT,
    filters JSONB,
    clicked_result_id UUID REFERENCES documents(id),
    clicked_position INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT search_history_id_unique UNIQUE (id)
);

-- ============================================================
-- Indexes for Performance
-- ============================================================

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);
CREATE INDEX IF NOT EXISTS idx_users_deleted_at ON users(deleted_at);

-- Categories indexes
CREATE INDEX IF NOT EXISTS idx_categories_is_active ON categories(is_active);
CREATE INDEX IF NOT EXISTS idx_categories_deleted_at ON categories(deleted_at);

-- Documents indexes
CREATE INDEX IF NOT EXISTS idx_documents_category_id ON documents(category_id);
CREATE INDEX IF NOT EXISTS idx_documents_created_by ON documents(created_by);
CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_deleted_at ON documents(deleted_at);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at DESC);

-- Conversations indexes
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_deleted_at ON conversations(deleted_at);

-- Messages indexes
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_rating ON messages(rating);

-- User activities indexes
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_activity_type ON user_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activities_created_at ON user_activities(created_at DESC);

-- Search history indexes
CREATE INDEX IF NOT EXISTS idx_search_history_user_id ON search_history(user_id);
CREATE INDEX IF NOT EXISTS idx_search_history_created_at ON search_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_search_history_query ON search_history USING gin(to_tsvector('english', query));

-- ============================================================
-- Success Message
-- ============================================================
\echo '✓ All tables created successfully!'
\echo 'Next: Run 03_seed_data.sql to populate initial data'
