"""Optional: run the raw SQL files against the database.

Usage:  python init_db.py            (schema only)
        python init_db.py --seed     (schema + sample data)
"""
import sys
from pathlib import Path

from sqlalchemy import text

from app.database import DATABASE_URL, engine

SQL_DIR = Path(__file__).parent / "sql"


def run_file(name: str):
    sql = (SQL_DIR / name).read_text()
    with engine.begin() as conn:
        for stmt in filter(None, (s.strip() for s in sql.split(";"))):
            conn.execute(text(stmt))
    print(f"Executed {name}")


if __name__ == "__main__":
    print("Using:", DATABASE_URL)
    run_file("schema_postgres.sql" if DATABASE_URL.startswith("postgres") else "schema.sql")
    if "--seed" in sys.argv:
        run_file("seed.sql")
