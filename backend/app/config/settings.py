"""
Application settings.

All configuration is read from environment variables (see .env.example at
the repository root). Nothing here is hardcoded application secret data -
only structural defaults for local development.
"""
from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

# Repository root .env (backend/app/config/settings.py -> repo root is 3 levels up).
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


def _get_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    # Shared MySQL database. Both perennia-auth and perennia-access run
    # their schema.sql against this same database (see backend/scripts/init_db.py).
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # perennia-auth
    auth_signing_secret: str
    require_email_verification: bool

    # Application
    cors_origins: list
    environment: str

    # Quotations workflow: the only two roles allowed to create, and to
    # approve, a quotation. Must name roles that exist in
    # app.permissions.definitions.ROLES.
    quotation_creator_role: str
    quotation_approver_role: str


def load_settings() -> Settings:
    signing_secret = os.getenv("AUTH_SIGNING_SECRET", "")
    if not signing_secret:
        raise RuntimeError(
            "AUTH_SIGNING_SECRET is not set. Copy .env.example to .env and set a long, "
            "random value before starting the application."
        )

    cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")

    return Settings(
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "3306")),
        db_user=os.getenv("DB_USER", "root"),
        db_password=os.getenv("DB_PASSWORD", ""),
        db_name=os.getenv("DB_NAME", "abc_enterprises"),
        auth_signing_secret=signing_secret,
        require_email_verification=_get_bool("REQUIRE_EMAIL_VERIFICATION", False),
        cors_origins=[o.strip() for o in cors_origins_raw.split(",") if o.strip()],
        environment=os.getenv("ENVIRONMENT", "development"),
        quotation_creator_role=os.getenv("QUOTATION_CREATOR_ROLE", "manager"),
        quotation_approver_role=os.getenv("QUOTATION_APPROVER_ROLE", "administrator"),
    )
