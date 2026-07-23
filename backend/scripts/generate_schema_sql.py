"""
(Re)generate backend/sql/schema.sql.

This does not define or duplicate any perennia-auth / perennia-access
table - it exports their own schema.sql files, verbatim, from whatever
version is currently installed, and concatenates them with a header. It
exists so the database can be set up with a SQL client alone (or by
whatever tooling reviews this repo), without needing to run Python.

The generated file is a convenience snapshot, not a second source of
truth: if the installed package version changes, re-run this script
rather than hand-editing backend/sql/schema.sql.

Usage (from backend/, with the virtualenv active):

    python scripts/generate_schema_sql.py
"""
import importlib.metadata
import importlib.resources
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


def _schema_sql(package: str) -> str:
    return importlib.resources.files(package).joinpath("schema.sql").read_text()


def main() -> None:
    auth_version = importlib.metadata.version("perennia-auth")
    access_version = importlib.metadata.version("perennia-access")

    parts = [
        "-- ABC Enterprises reference application - combined database schema.\n"
        "--\n"
        "-- GENERATED FILE - do not hand-edit.\n"
        "-- Produced by backend/scripts/generate_schema_sql.py, which exports the\n"
        "-- schema.sql shipped inside the installed perennia-auth and\n"
        "-- perennia-access packages, unmodified. Re-run that script after\n"
        "-- upgrading either dependency instead of editing this file directly.\n"
        f"-- perennia-auth   version: {auth_version}\n"
        f"-- perennia-access version: {access_version}\n"
        "--\n"
        "-- Apply with: mysql -u <user> -p <database> < backend/sql/schema.sql\n"
        "-- (equivalent to running backend/scripts/init_db.py)\n",
        f"\n-- ============================================================\n"
        f"-- perennia-auth {auth_version} (source: https://github.com/BT-Rajan/perennia-auth)\n"
        f"-- ============================================================\n"
        + _schema_sql("perennia_auth"),
        f"\n-- ============================================================\n"
        f"-- perennia-access {access_version} (source: https://github.com/BT-Rajan/perennia-access)\n"
        f"-- ============================================================\n"
        + _schema_sql("perennia_access"),
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(parts))
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
