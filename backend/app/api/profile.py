from fastapi import APIRouter, Depends

from perennia_access import AuthenticatedIdentity

from app.deps import access, require_permission
from app.permissions.definitions import PROFILE_VIEW
from app.schemas import ProfileResponse

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
def profile(identity: AuthenticatedIdentity = Depends(require_permission(PROFILE_VIEW))):
    roles = access.get_identity_roles(identity)
    return ProfileResponse(subject_id=identity.subject_id, roles=roles)
