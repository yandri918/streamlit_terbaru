"""
CLI Migration Tool — Migrate Local SQLite Data to Cloud PostgreSQL
Usage:
    python utils/migrate_to_postgres.py [POSTGRES_DATABASE_URL]
    
Example:
    python utils/migrate_to_postgres.py postgresql://postgres:mypassword@junction.proxy.rlwy.net:12345/railway
"""
import sys
import os
import sqlite3
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.config import settings

SQLITE_PATH = ROOT_DIR / "krisan.db"
PG_SCHEMA_PATH = ROOT_DIR / "database" / "01_postgres_schema.sql"


def migrate(target_url: str):
    import psycopg2
    from psycopg2.extras import RealDictCursor

    if target_url.startswith("postgres://"):
        target_url = "postgresql://" + target_url[len("postgres://"):]

    print(f"==================================================")
    print(f"🌸 BUDIDAYA KRISAN PRO — CLOUD MIGRATION TOOL")
    print(f"==================================================")
    print(f"📁 Source SQLite:      {SQLITE_PATH}")
    print(f"☁️ Target PostgreSQL:  {target_url.split('@')[-1] if '@' in target_url else target_url}")

    if not SQLITE_PATH.exists():
        print(f"❌ Error: File SQLite {SQLITE_PATH} tidak ditemukan.")
        return

    # 1. Connect to SQLite
    sqlite_conn = sqlite3.connect(str(SQLITE_PATH))
    sqlite_conn.row_factory = sqlite3.Row

    # 2. Connect to PostgreSQL
    try:
        pg_conn = psycopg2.connect(target_url, cursor_factory=RealDictCursor)
        print("✅ Terhubung ke PostgreSQL Cloud.")
    except Exception as e:
        print(f"❌ Gagal koneksi ke PostgreSQL: {e}")
        return

    # 3. Create Schema on PostgreSQL
    try:
        with pg_conn.cursor() as cur:
            if PG_SCHEMA_PATH.exists():
                print("⚙️ Menerapkan skema tabel PostgreSQL...")
                cur.execute(PG_SCHEMA_PATH.read_text(encoding="utf-8"))
        pg_conn.commit()
        print("✅ Skema database berhasil dibuat/diverifikasi.")
    except Exception as e:
        pg_conn.rollback()
        print(f"❌ Gagal membuat skema PostgreSQL: {e}")
        return

    # 4. Migrate tables in topological order
    tables = [
        "varieties",
        "cultivation_batches",
        "growth_records",
        "harvest_records",
        "harvest_detail_grades",
        "cost_journal",
        "webhook_config",
    ]

    total_migrated = 0

    for table in tables:
        try:
            rows = sqlite_conn.execute(f"SELECT * FROM {table}").fetchall()
            if not rows:
                print(f"ℹ️  Tabel {table:<22} : 0 data (dilewati)")
                continue

            columns = [k for k in rows[0].keys()]
            cols_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))

            # Conflict target is id (primary key)
            insert_sql = (
                f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders}) "
                f"ON CONFLICT (id) DO NOTHING"
            )

            with pg_conn.cursor() as cur:
                count = 0
                for row in rows:
                    values = tuple(row[col] for col in columns)
                    cur.execute(insert_sql, values)
                    count += 1

            pg_conn.commit()
            print(f"✅ Tabel {table:<22} : {count} data berhasil disinkronisasi")
            total_migrated += count

        except Exception as e:
            pg_conn.rollback()
            print(f"⚠️  Peringatan pada tabel {table}: {e}")

    sqlite_conn.close()
    pg_conn.close()

    print(f"==================================================")
    print(f"🎉 Migrasi selesai! Total {total_migrated} record disalin ke Cloud.")
    print(f"==================================================")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_db_url = sys.argv[1]
    else:
        target_db_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL

    if not target_db_url or target_db_url.startswith("sqlite"):
        print("Penggunaan:")
        print("  python utils/migrate_to_postgres.py <DATABASE_URL_POSTGRES>")
        print("\nContoh:")
        print("  python utils/migrate_to_postgres.py postgresql://postgres:password@junction.proxy.rlwy.net:12345/railway")
        sys.exit(1)

    migrate(target_db_url)
