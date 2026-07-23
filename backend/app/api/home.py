from fastapi import APIRouter, Depends

from perennia_access import AuthenticatedIdentity

from app.deps import access, get_current_identity
from app.permissions.definitions import PROFILE_VIEW, REPORTS_VIEW, ADMIN_ACCESS, SEARCH_ACCESS, FILES_VIEW
from app.schemas import HomeResponse, AreaSummary

router = APIRouter(prefix="/api/home", tags=["home"])

# Declared once; drives both what /api/home reports and (indirectly, via the
# same permission codes) what each protected route itself enforces.
_AREAS = [
    ("profile", "Profile", "/profile", PROFILE_VIEW),
    ("reports", "Reports", "/reports", REPORTS_VIEW),
    ("search", "Search", "/search", SEARCH_ACCESS),
    ("files", "Files", "/files", FILES_VIEW),
    ("administration", "Administration", "/administration", ADMIN_ACCESS),
]


@router.get("", response_model=HomeResponse)
def home(identity: AuthenticatedIdentity = Depends(get_current_identity)):
    roles = access.get_identity_roles(identity)
    granted = set(access.get_identity_permissions(identity))

    areas = [
        AreaSummary(key=key, label=label, path=path, permission=permission, available=permission in granted)
        for key, label, path, permission in _AREAS
    ]
    return HomeResponse(subject_id=identity.subject_id, roles=roles, areas=areas)
