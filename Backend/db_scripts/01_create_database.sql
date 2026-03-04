-- ============================================================
-- Legal Assistant Database Setup
-- ============================================================
-- This script creates the database and enables required extensions
-- Run this as a PostgreSQL superuser (e.g., postgres)
-- ============================================================

-- Create database (if it doesn't exist)
-- Note: You may need to run this separately as you can't create a database from within a database
-- CREATE DATABASE legal_assist;

-- Connect to the database
\c legal_assist;

-- ============================================================
-- Enable Required Extensions
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector for vector similarity search
-- Make sure pgvector is installed on your PostgreSQL server
-- Installation: https://github.com/pgvector/pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extensions
SELECT * FROM pg_extension WHERE extname IN ('uuid-ossp', 'vector');

-- ============================================================
-- Success Message
-- ============================================================
\echo '✓ Database and extensions created successfully!'
\echo 'Next: Run 02_create_tables.sql'
