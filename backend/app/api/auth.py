from fastapi import APIRouter, Depends, Request

from perennia_access import AuthenticatedIdentity

from app.deps import auth, access, get_current_identity
from app.schemas import (
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    GenericMessageResponse,
    MeResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/register", response_model=RegisterResponse)
def register(body: RegisterRequest, request: Request):
    subject_id = auth.register(
        body.email,
        body.password,
        ip_address=_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    # Demo-only: the registration form lets the visitor pick which of the
    # three example roles to explore. In a real application this would be
    # an internal admin action, not a self-service choice - see README.
    access.assign_role_to_user(subject_id, body.role)
    return RegisterResponse(
        message=(
            "Account created. Check the backend console for your verification "
            "link (this demo sends email via console output, not SMTP)."
        )
    )


@router.post("/verify-email", response_model=GenericMessageResponse)
def verify_email(body: VerifyEmailRequest, request: Request):
    auth.verify_email(body.token, ip_address=_client_ip(request), user_agent=request.headers.get("user-agent"))
    return GenericMessageResponse(message="Email verified. You can now sign in.")


@router.post("/resend-verification", response_model=GenericMessageResponse)
def resend_verification(body: ForgotPasswordRequest, request: Request):
    auth.resend_verification(body.email, ip_address=_client_ip(request), user_agent=request.headers.get("user-agent"))
    # Generic response regardless of whether the email exists or is already verified.
    return GenericMessageResponse(message="If that email exists and is unverified, a new link has been sent.")


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, request: Request):
    result = auth.authenticate(
        body.email,
        body.password,
        ip_address=_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        access_token_expires_at=result.access_token_expires_at,
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh(body: RefreshRequest, request: Request):
    result = auth.refresh(
        body.refresh_token,
        ip_address=_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    return RefreshResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        access_token_expires_at=result.access_token_expires_at,
    )


@router.post("/logout", response_model=GenericMessageResponse)
def logout(
    request: Request,
    identity: AuthenticatedIdentity = Depends(get_current_identity),
):
    auth.logout(identity.session_id, ip_address=_client_ip(request), user_agent=request.headers.get("user-agent"))
    return GenericMessageResponse(message="Signed out.")


@router.post("/forgot-password", response_model=GenericMessageResponse)
def forgot_password(body: ForgotPasswordRequest, request: Request):
    auth.request_password_recovery(
        body.email, ip_address=_client_ip(request), user_agent=request.headers.get("user-agent")
    )
    # Always the same response - never reveal whether the address exists.
    return GenericMessageResponse(
        message="If that email is registered, password reset instructions have been sent."
    )


@router.post("/reset-password", response_model=GenericMessageResponse)
def reset_password(body: ResetPasswordRequest, request: Request):
    auth.reset_password(
        body.token,
        body.new_password,
        ip_address=_client_ip(request),
        user_agent=request.headers.get("user-agent"),
    )
    return GenericMessageResponse(message="Password reset. You can now sign in with your new password.")


@router.get("/me", response_model=MeResponse)
def me(identity: AuthenticatedIdentity = Depends(get_current_identity)):
    roles = access.get_identity_roles(identity)
    permissions = access.get_identity_permissions(identity)
    return MeResponse(
        subject_id=identity.subject_id,
        session_id=identity.session_id,
        roles=roles,
        permissions=permissions,
    )
