"""
Shared FastAPI dependencies.

This is the integration seam described in the architecture: every
protected route depends on `get_current_identity` (perennia-auth) and,
where authorization matters, `require_permission(...)` (perennia-access).
No route implements its own token parsing or its own role checks.
"""
from fastapi import Depends, Header

from perennia_auth import (
    PerenniaAuth,
    AuthConfig,
    DatabaseConfig as AuthDatabaseConfig,
)
from perennia_access import (
    PerenniaAccess,
    AccessConfig,
    DatabaseConfig as AccessDatabaseConfig,
    AuthenticatedIdentity,
)

from app.config.settings import load_settings
from app.config.errors import AppError
from app.mailer import ConsoleMailer

settings = load_settings()

auth = PerenniaAuth(
    AuthConfig(
        signing_secret=settings.auth_signing_secret,
        database=AuthDatabaseConfig(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
        ),
        require_email_verification=settings.require_email_verification,
    ),
    mailer=ConsoleMailer(frontend_base_url="http://localhost:5173"),
)

access = PerenniaAccess(
    AccessConfig(
        database=AccessDatabaseConfig(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
        ),
    )
)


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AppError("authentication_required")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise AppError("authentication_required")
    return token


def get_current_identity(
    authorization: str | None = Header(default=None),
) -> AuthenticatedIdentity:
    """Authenticate the request via perennia-auth and return the
    AuthenticatedIdentity contract perennia-access expects.

    Deliberately does not touch perennia-access - authentication and
    authorization stay in separate steps, with no second token exchange
    between the two packages.
    """
    token = _extract_bearer_token(authorization)
    # verify_access_token raises ExpiredTokenError / InvalidTokenError,
    # both perennia-auth exceptions, on failure. They propagate to the
    # global exception handler in app.main and are resolved through the
    # central error catalog - this dependency does not translate them itself.
    claims = auth.verify_access_token(token)
    return AuthenticatedIdentity(subject_id=claims["sub"], session_id=claims["sid"])


def require_permission(permission_code: str):
    """Dependency factory: require a specific permission via perennia-access.

    Usage: `identity = Depends(require_permission("reports.view"))`
    """

    def _dependency(
        identity: AuthenticatedIdentity = Depends(get_current_identity),
    ) -> AuthenticatedIdentity:
        # access.require raises AuthorizationDenied / PermissionNotFoundError /
        # AccessDatabaseError - all perennia-access exceptions - on failure.
        # They propagate to the global handler, same as above.
        access.require(identity, permission_code)
        return identity

    return _dependency
