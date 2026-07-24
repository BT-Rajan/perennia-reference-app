"""
Seed login-ready demo accounts.

backend/sql/test_data.sql covers the perennia-access side (permissions and
roles) with plain SQL. It deliberately stops there: a real login-ready
account needs a password hash produced by perennia-auth's own hashing code,
and reproducing that in hand-written SQL would mean reimplementing
authentication - exactly what this application is built to avoid.

This script instead drives the actual public APIs - the same ones
app/api/auth.py uses - to create three demo accounts, one per role, and
auto-verifies them by capturing perennia-auth's own verification token
in-process (standing in for clicking the email link). Safe to re-run:
existing accounts are skipped.

Usage (from backend/, with the virtualenv active and .env configured):

    python scripts/seed_demo_data.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from perennia_auth import PerenniaAuth, AuthConfig, DatabaseConfig as AuthDatabaseConfig
from perennia_auth import EmailAlreadyExistsError
from perennia_access import PerenniaAccess, AccessConfig, DatabaseConfig as AccessDatabaseConfig

from app.config.settings import load_settings
from app.permissions import definitions as permission_definitions

DEMO_ACCOUNTS = [
    ("employee.demo@abc-enterprises.example", "DemoPass123", "employee"),
    ("manager.demo@abc-enterprises.example", "DemoPass123", "manager"),
    ("administrator.demo@abc-enterprises.example", "DemoPass123", "administrator"),
]


class CapturingMailer:
    """Stands in for a real mailer: captures the raw verification token
    instead of sending it anywhere, so this script can verify the account
    itself in the same process."""

    def __init__(self):
        self.last_verification_token = None

    def send_verification_email(self, email: str, raw_token: str) -> None:
        self.last_verification_token = raw_token

    def send_email_change_verification(self, new_email: str, raw_token: str) -> None:
        pass

    def send_password_recovery_email(self, email: str, raw_token: str) -> None:
        pass

    def notify_email_changed(self, old_email: str, new_email: str) -> None:
        pass


def main() -> None:
    settings = load_settings()
    mailer = CapturingMailer()

    auth = PerenniaAuth(
        AuthConfig(
            signing_secret=settings.auth_signing_secret,
            database=AuthDatabaseConfig(
                host=settings.db_host, port=settings.db_port, user=settings.db_user,
                password=settings.db_password, database=settings.db_name,
            ),
            require_email_verification=settings.require_email_verification,
        ),
        mailer=mailer,
    )
    access = PerenniaAccess(
        AccessConfig(
            database=AccessDatabaseConfig(
                host=settings.db_host, port=settings.db_port, user=settings.db_user,
                password=settings.db_password, database=settings.db_name,
            )
        )
    )

    # Ensure the permission vocabulary and demo roles exist first.
    permission_definitions.seed(access, settings)

    print(f"{'Email':45} {'Role':15} Status")
    print("-" * 75)
    for email, password, role in DEMO_ACCOUNTS:
        try:
            subject_id = auth.register(email, password)
        except EmailAlreadyExistsError:
            print(f"{email:45} {role:15} already exists - skipped")
            continue

        auth.verify_email(mailer.last_verification_token)
        access.assign_role_to_user(subject_id, role)
        print(f"{email:45} {role:15} created + verified")

    print("\nDemo credentials (password is the same for all three):")
    for email, password, role in DEMO_ACCOUNTS:
        print(f"  {role:15} {email:45} {password}")


if __name__ == "__main__":
    main()
