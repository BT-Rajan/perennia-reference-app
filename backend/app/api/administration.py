from fastapi import APIRouter, Depends

from perennia_access import AuthenticatedIdentity

from app.deps import require_permission
from app.permissions.definitions import ADMIN_ACCESS
from app.schemas import AdministrationResponse

router = APIRouter(prefix="/api/administration", tags=["administration"])


@router.get("", response_model=AdministrationResponse)
def administration(identity: AuthenticatedIdentity = Depends(require_permission(ADMIN_ACCESS))):
    # Demonstration only - no real administrative functionality. See project scope in README.
    return AdministrationResponse(message="You have administrative access.")
