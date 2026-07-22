"""
One-time database setup.

Creates the application database (if needed) and applies the schema.sql
files shipped inside the installed perennia_auth and perennia_access
packages - unmodified, straight from the packages themselves. This script
does not define or duplicate any of their tables; it just runs their SQL.

Usage (from backend/, with the virtualenv active and .env configured):

    python scripts/init_db.py
"""
import importlib.resources
import os
import sys

import pymysql
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def _schema_sql(package: str) -> str:
    return importlib.resources.files(package).joinpath("schema.sql").read_text()


def main() -> None:
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "abc_enterprises")

    print(f"Connecting to MySQL at {host}:{port} as {user} ...")
    conn = pymysql.connect(host=host, port=port, user=user, password=password, charset="utf8mb4")
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.commit()
    finally:
        conn.close()

    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset="utf8mb4")
    try:
        for package, label in (("perennia_auth", "perennia-auth"), ("perennia_access", "perennia-access")):
            print(f"Applying schema from {label} ...")
            sql = _schema_sql(package)
            with conn.cursor() as cur:
                for statement in sql.split(";"):
                    statement = statement.strip()
                    if statement:
                        cur.execute(statement)
            conn.commit()
        print("Database schema is up to date.")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - operator-facing script
        print(f"Database initialization failed: {exc}", file=sys.stderr)
        sys.exit(1)
