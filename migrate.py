import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Missing DATABASE_URL. Please check your .env file.")

MIGRATIONS_DIR = Path("migrations")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMPTZ DEFAULT now() NOT NULL
            );
        """)
    conn.commit()

def get_applied_migrations(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT migration_name FROM schema_migrations;")
        return {row[0] for row in cur.fetchall()}
    
def run_migrations():
    conn = get_connection()

    try:
        create_migrations_table(conn)
        applied = get_applied_migrations(conn)
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

        for migration_file in migration_files:
            file_name = migration_file.name
            if file_name in applied:
                print(f"Skipping{file_name} (already applied)")
                continue

            print(f"Applying {file_name}...")
            sql = migration_file.read_text(encoding="utf-8")

            try:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    cur.execute(
                        "INSERT INTO schema_migrations (migration_name) VALUES (%s);",
                        (file_name,)
                    )
                conn.commit()
                print(f"Successfully applied: {file_name}")
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Failed on {file_name}. Changes rolled back.")
                print(f"Error: {e}")
                break

    finally:
        conn.close()


if __name__ == "__main__":
    run_migrations()