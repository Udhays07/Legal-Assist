-- ============================================================
-- Legal Assistant - Database Cleanup Script
-- ============================================================
-- WARNING: This script will delete ALL data from the database
-- Use with caution! Only run this if you want to reset the database
-- ============================================================

\c legal_assist;

-- ============================================================
-- Confirm Before Running
-- ============================================================

\echo '⚠️  WARNING: This will delete ALL data from the database!'
\echo 'Press Ctrl+C to cancel, or press Enter to continue...'
\prompt 'Type YES to confirm: ' confirmation

-- ============================================================
-- Drop All Tables (in correct order due to foreign keys)
-- ============================================================

\echo 'Dropping tables...'

DROP TABLE IF EXISTS search_history CASCADE;
DROP TABLE IF EXISTS user_activities CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS document_embeddings CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

\echo '✓ All tables dropped'

-- ============================================================
-- Optional: Drop Extensions
-- ============================================================

-- Uncomment if you want to remove extensions as well
-- DROP EXTENSION IF EXISTS vector;
-- DROP EXTENSION IF EXISTS "uuid-ossp";

-- ============================================================
-- Success Message
-- ============================================================

\echo ''
\echo '✓ Database cleaned successfully!'
\echo ''
\echo 'To recreate the database:'
\echo '1. Run: psql -U postgres -f 02_create_tables.sql'
\echo '2. Run: psql -U postgres -f 03_seed_data.sql'
