"""
Database Manager — Budidaya Krisan Pro
Dual-Engine Support:
- SQLite (Local development & offline field usage)
- PostgreSQL (Production cloud on Railway / Supabase / Neon)
"""
import os
import re
import sqlite3
import uuid
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import settings

logger = logging.getLogger("app.db")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_DB_PATH = BASE_DIR / "krisan.db"
PG_SCHEMA_PATH = BASE_DIR / "database" / "01_postgres_schema.sql"
PG_SEEDS_PATH = BASE_DIR / "database" / "02_postgres_seeds.sql"
SQLITE_SCHEMA_PATH = BASE_DIR / "database" / "01_schema.sql"
SQLITE_SEEDS_PATH = BASE_DIR / "database" / "02_seeds.sql"

_initialized = False


def get_database_url() -> str:
    """Retrieve normalized database URL from settings or environment."""
    url = os.getenv("DATABASE_URL") or settings.DATABASE_URL or "sqlite:///./krisan.db"
    # Railway/Heroku sometimes supply postgres:// instead of postgresql://
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


def is_postgres() -> bool:
    """Check if current active configuration targets PostgreSQL."""
    url = get_database_url()
    return url.startswith("postgresql://")


class PostgresCursorWrapper:
    """Wrapper around psycopg2 cursor for SQLite-compatible execution."""
    def __init__(self, cursor):
        self._cur = cursor

    def fetchone(self) -> Optional[Dict[str, Any]]:
        row = self._cur.fetchone()
        return dict(row) if row else None

    def fetchall(self) -> List[Dict[str, Any]]:
        rows = self._cur.fetchall()
        return [dict(r) for r in rows] if rows else []

    @property
    def rowcount(self) -> int:
        return self._cur.rowcount


class PostgresConnectionWrapper:
    """Wrapper around psycopg2 connection matching sqlite3 connection interface."""
    def __init__(self, conn):
        self._conn = conn
        self._last_cursor = None

    def execute(self, sql: str, params: Optional[Any] = None) -> PostgresCursorWrapper:
        # Translate ? parameter placeholders to %s
        translated_sql = sql.replace("?", "%s")
        cur = self._conn.cursor()
        self._last_cursor = cur
        if params is not None:
            if isinstance(params, list):
                cur.execute(translated_sql, tuple(params))
            else:
                cur.execute(translated_sql, params)
        else:
            cur.execute(translated_sql)
        return PostgresCursorWrapper(cur)

    def executescript(self, script: str):
        with self._conn.cursor() as cur:
            cur.execute(script)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        if self._last_cursor and not self._last_cursor.closed:
            self._last_cursor.close()
        self._conn.close()


@contextmanager
def get_db():
    """Yield a database connection (SQLite or PostgreSQL) with auto-commit/rollback."""
    global _initialized
    if not _initialized:
        _initialized = True
        init_db()

    url = get_database_url()

    if is_postgres():
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(url, cursor_factory=RealDictCursor)
        wrapper = PostgresConnectionWrapper(conn)
        try:
            yield wrapper
            wrapper.commit()
        except Exception:
            wrapper.rollback()
            raise
        finally:
            wrapper.close()
    else:
        conn = sqlite3.connect(str(SQLITE_DB_PATH))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db():
    """Initialize database schema and seed data on startup."""
    if is_postgres():
        _init_postgres()
    else:
        _init_sqlite()


def _init_postgres():
    """Initialize PostgreSQL tables & seeds in the cloud."""
    import psycopg2
    from psycopg2.extras import RealDictCursor
    url = get_database_url()
    logger.info("Initializing PostgreSQL Cloud Database...")

    conn = psycopg2.connect(url, cursor_factory=RealDictCursor)
    try:
        with conn.cursor() as cur:
            if PG_SCHEMA_PATH.exists():
                cur.execute(PG_SCHEMA_PATH.read_text(encoding="utf-8"))
            if PG_SEEDS_PATH.exists():
                cur.execute(PG_SEEDS_PATH.read_text(encoding="utf-8"))
        conn.commit()
        logger.info("PostgreSQL Cloud Database initialized successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"PostgreSQL initialization failed: {e}")
        raise e
    finally:
        conn.close()


def _init_sqlite():
    """Initialize SQLite tables & seeds locally."""
    if SQLITE_SCHEMA_PATH.exists():
        schema_sql = SQLITE_SCHEMA_PATH.read_text(encoding="utf-8")
    else:
        schema_sql = ""

    with get_db() as conn:
        if schema_sql:
            conn.executescript(schema_sql)
        if SQLITE_SEEDS_PATH.exists():
            try:
                conn.executescript(SQLITE_SEEDS_PATH.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"SQLite seed script warning: {e}")

        # Ensure greenhouse columns exist on legacy databases
        batch_cols = [c[1] for c in conn.execute("PRAGMA table_info(cultivation_batches)").fetchall()]
        if "house_name" not in batch_cols:
            conn.execute("ALTER TABLE cultivation_batches ADD COLUMN house_name TEXT DEFAULT 'House 1'")
        if "beds_count" not in batch_cols:
            conn.execute("ALTER TABLE cultivation_batches ADD COLUMN beds_count INTEGER DEFAULT 12")
        if "bed_length_m" not in batch_cols:
            conn.execute("ALTER TABLE cultivation_batches ADD COLUMN bed_length_m REAL DEFAULT 50.0")


def get_db_info() -> Dict[str, Any]:
    """Return database engine status metadata."""
    if is_postgres():
        url = get_database_url()
        # Mask credentials in output
        masked = re.sub(r"://([^:]+):([^@]+)@", r"://\1:****@", url)
        return {
            "engine": "postgresql",
            "type": "Cloud PostgreSQL (Railway / Supabase / Neon)",
            "url": masked,
            "status": "connected",
        }
    else:
        return {
            "engine": "sqlite",
            "type": "SQLite Local (Offline Capable)",
            "path": str(SQLITE_DB_PATH),
            "status": "connected",
        }


def new_id() -> str:
    """Generate a clean UUID string."""
    return str(uuid.uuid4())


def row_to_dict(row: Any) -> dict:
    """Convert a row factory object to dictionary."""
    return dict(row) if row else {}


def rows_to_list(rows: Any) -> list:
    """Convert an iterable of rows to a list of dicts."""
    return [dict(r) for r in rows] if rows else []
