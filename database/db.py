import os
from contextlib import contextmanager
from dotenv import load_dotenv
from psycopg2.pool import ThreadedConnectionPool
import psycopg2

# Load environment variables once
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

_pool: ThreadedConnectionPool | None = None


def _ensure_pool(minconn: int = 1, maxconn: int = 10) -> ThreadedConnectionPool:
    global _pool
    if _pool is None:
        dsn = (
            f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} "
            f"host={DB_HOST} port={DB_PORT}"
        )
        _pool = ThreadedConnectionPool(minconn=minconn, maxconn=maxconn, dsn=dsn)
    return _pool


def get_connection() -> psycopg2.extensions.connection:
    pool = _ensure_pool()
    return pool.getconn()


def put_connection(conn: psycopg2.extensions.connection) -> None:
    pool = _ensure_pool()
    pool.putconn(conn)


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None


@contextmanager
def get_cursor(autocommit: bool = False):
    conn = get_connection()
    original_autocommit = conn.autocommit
    try:
        conn.autocommit = autocommit
        cur = conn.cursor()
        try:
            yield cur
            if not autocommit:
                conn.commit()
        except Exception:
            if not autocommit:
                conn.rollback()
            raise
        finally:
            cur.close()
    finally:
        conn.autocommit = original_autocommit
        put_connection(conn)


