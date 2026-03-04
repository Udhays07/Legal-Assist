-- ============================================================
-- Legal Assistant - Seed Data Script
-- ============================================================
-- Populates initial data for roles and sample users
-- Run this after 02_create_tables.sql
-- ============================================================

\c legal_assist;

-- ============================================================
-- Seed Roles
-- ============================================================

INSERT INTO roles (id, name) VALUES
    ('11111111-1111-1111-1111-111111111111', 'admin'),
    ('22222222-2222-2222-2222-222222222222', 'user')
ON CONFLICT (name) DO NOTHING;

\echo '✓ Roles seeded'

-- ============================================================
-- Seed Sample Users
-- ============================================================

-- Admin user
INSERT INTO users (id, name, role_id) VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Admin User', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (id) DO NOTHING;

-- Regular user (for testing)
INSERT INTO users (id, name, role_id) VALUES
    ('123e4567-e89b-12d3-a456-426614174000', 'Test User', '22222222-2222-2222-2222-222222222222')
ON CONFLICT (id) DO NOTHING;

\echo '✓ Sample users seeded'

-- ============================================================
-- Seed Sample Categories
-- ============================================================

INSERT INTO categories (id, title, description, is_active) VALUES
    ('cat11111-1111-1111-1111-111111111111', 'Indian Penal Code', 'Sections and provisions from the Indian Penal Code', true),
    ('cat22222-2222-2222-2222-222222222222', 'Insurance Law', 'Insurance policies, claims, and regulations', true),
    ('cat33333-3333-3333-3333-333333333333', 'Contract Law', 'Contract provisions, clauses, and legal agreements', true),
    ('cat44444-4444-4444-4444-444444444444', 'Property Law', 'Real estate, property rights, and transactions', true)
ON CONFLICT (title) DO NOTHING;

\echo '✓ Sample categories seeded'

-- ============================================================
-- Seed Sample Documents
-- ============================================================

-- IPC Section 302
INSERT INTO documents (id, category_id, title, content, tags, status, created_by) VALUES
    ('doc11111-1111-1111-1111-111111111111',
     'cat11111-1111-1111-1111-111111111111',
     'Section 302 IPC - Punishment for Murder',
     'Section 302 of the Indian Penal Code deals with "Punishment for Murder". It states that whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine. This is one of the most serious offenses under the IPC and carries the maximum penalty. The section applies to all cases where murder has been established beyond reasonable doubt.',
     ARRAY['ipc', 'criminal law', 'murder', 'section 302'],
     'published',
     'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
ON CONFLICT (id) DO NOTHING;

-- IPC Section 420
INSERT INTO documents (id, category_id, title, content, tags, status, created_by) VALUES
    ('doc22222-2222-2222-2222-222222222222',
     'cat11111-1111-1111-1111-111111111111',
     'Section 420 IPC - Cheating and Dishonestly Inducing Delivery of Property',
     'Section 420 of the Indian Penal Code deals with cheating and dishonestly inducing delivery of property. Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.',
     ARRAY['ipc', 'criminal law', 'fraud', 'cheating', 'section 420'],
     'published',
     'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
ON CONFLICT (id) DO NOTHING;

-- Insurance Claims
INSERT INTO documents (id, category_id, title, content, tags, status, created_by) VALUES
    ('doc33333-3333-3333-3333-333333333333',
     'cat22222-2222-2222-2222-222222222222',
     'Insurance Claims Settlement Procedures',
     'Insurance claims settlement is the process by which an insurance company pays out benefits to a policyholder or their beneficiary. The insurer must investigate the claim, verify coverage, assess damages, and determine the appropriate payout amount. Insurers are required by law to handle claims in good faith and cannot unreasonably delay or deny valid claims. Unfair claims practices include misrepresenting policy provisions, failing to acknowledge claims promptly, not conducting reasonable investigations, and offering substantially less than amounts due.',
     ARRAY['insurance', 'claims', 'settlement', 'procedures'],
     'published',
     'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')
ON CONFLICT (id) DO NOTHING;

\echo '✓ Sample documents seeded'

-- ============================================================
-- Verify Seeded Data
-- ============================================================

\echo ''
\echo '=== Database Summary ==='
SELECT 'Roles' as table_name, COUNT(*) as count FROM roles
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Documents', COUNT(*) FROM documents;

\echo ''
\echo '✓ Database seeded successfully!'
\echo ''
\echo 'Default Test User ID: 123e4567-e89b-12d3-a456-426614174000'
\echo 'Use this user_id for testing the RAG API'
\echo ''
\echo 'Next steps:'
\echo '1. Update Backend/.env with your database credentials'
\echo '2. Run: cd Backend && python -m uvicorn app.main:app --reload'
\echo '3. Visit: http://localhost:8000/docs'
