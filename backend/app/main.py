import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from perennia_auth import PerenniaAuthError
from perennia_access import AccessError

from app.config.errors import AppError, resolve
from app.deps import settings, access
from app.permissions import definitions as permission_definitions
from app.api import auth, home, profile, reports, administration, search, files, crud, crud_bulk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("abc_enterprises")

app = FastAPI(title="ABC Enterprises Reference API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(profile.router)
app.include_router(reports.router)
app.include_router(administration.router)
app.include_router(search.router)
app.include_router(files.router)
app.include_router(crud.router)
app.include_router(crud_bulk.router)


@app.on_event("startup")
def seed_permissions() -> None:
    """Idempotently create the application's permission vocabulary and demo
    roles in perennia-access. Safe to run on every startup."""
    permission_definitions.seed(access)
    logger.info("Permission and role seed complete.")


def _error_response(code: str, request_id_hint: str | None = None) -> JSONResponse:
    spec = resolve(code)
    return JSONResponse(status_code=spec.http_status, content={"error": {"code": code, "message": spec.message}})


# --- Centralized error handling ---------------------------------------------
# Every handler below does the same thing: take whatever failed, resolve it
# to a stable error code, and look that code up in app.config.errors. No
# handler constructs its own message or status code - the catalog is the
# single source of truth referenced everywhere in this file.

@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    return _error_response(exc.code)


@app.exception_handler(PerenniaAuthError)
def handle_auth_error(request: Request, exc: PerenniaAuthError):
    return _error_response(getattr(exc, "code", "auth_error"))


@app.exception_handler(AccessError)
def handle_access_error(request: Request, exc: AccessError):
    code = getattr(exc, "code", "access_error")
    if code in ("permission_not_found", "role_not_found", "invalid_access_configuration"):
        # Configuration errors are ours, not the user's - log details server-side,
        # but never expose them to the client.
        logger.error("Access configuration error: %s", exc)
    return _error_response(code)


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    return _error_response("validation_error")


@app.exception_handler(StarletteHTTPException)
def handle_http_exception(request: Request, exc: StarletteHTTPException):
    # Framework-level failures (unmatched route, wrong method, etc.) - map
    # the small set we care about onto the catalog; anything else falls
    # back to a generic message rather than echoing Starlette's own text.
    if exc.status_code == 404:
        return _error_response("not_found")
    spec = resolve("http_error")
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": "http_error", "message": spec.message}})


@app.exception_handler(Exception)
def handle_unexpected_error(request: Request, exc: Exception):
    # Never leak tracebacks, SQL, file paths, or raw driver errors to the client.
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return _error_response("internal_error")


@app.get("/api/health")
def health():
    return {"status": "ok"}
