from fastapi import APIRouter, Depends

from perennia_access import AuthenticatedIdentity

from app.deps import require_permission
from app.permissions.definitions import REPORTS_VIEW
from app.schemas import ReportsResponse

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("", response_model=ReportsResponse)
def reports(identity: AuthenticatedIdentity = Depends(require_permission(REPORTS_VIEW))):
    # Demonstration only - no real report data. See project scope in README.
    return ReportsResponse(message="You have access to the reports area.")
