from database.db import get_cursor

migration_sql = """
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS pokemon (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL,
    height INT,
    weight INT
);
"""

def run_migration():
    try:
        with get_cursor(autocommit=True) as cur:
            cur.execute(migration_sql)
        print("✅ Migration applied successfully")
    except Exception as e:
        print("❌ Migration failed:", e)

if __name__ == "__main__":
    run_migration()