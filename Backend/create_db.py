"""Helper script to create the legal_assist database if it doesn't exist and enable pgvector."""
import psycopg2
import sys

DB_URL = "postgresql://postgres:sql@localhost:5432/postgres"
DB_NAME = "legal_assist"

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if cur.fetchone():
        print(f"Database '{DB_NAME}' already exists.")
    else:
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"Database '{DB_NAME}' created.")

    cur.close()
    conn.close()

    # Connect to the new DB to enable pgvector extension
    conn2 = psycopg2.connect(f"postgresql://postgres:sql@localhost:5432/{DB_NAME}")
    conn2.autocommit = True
    cur2 = conn2.cursor()
    cur2.execute("CREATE EXTENSION IF NOT EXISTS vector")
    print("pgvector extension enabled.")
    cur2.close()
    conn2.close()

    print("DB setup complete.")
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
