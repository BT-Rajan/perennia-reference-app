from fastapi import APIRouter, Depends

from perennia_access import AuthenticatedIdentity

from app.deps import access, get_current_identity
from app.permissions.definitions import (
    PROFILE_VIEW, REPORTS_VIEW, ADMIN_ACCESS, SEARCH_ACCESS, FILES_VIEW,
    CLIENTS_READ, PRODUCTS_READ, RAW_MATERIALS_READ, SUPPLIERS_READ, QUOTATIONS_READ,
)
from app.schemas import HomeResponse, AreaSummary

router = APIRouter(prefix="/api/home", tags=["home"])

# Declared once; drives both what /api/home reports and (indirectly, via the
# same permission codes) what each protected route itself enforces.
_AREAS = [
    ("profile", "Profile", "/profile", PROFILE_VIEW),
    ("reports", "Reports", "/reports", REPORTS_VIEW),
    ("search", "Search", "/search", SEARCH_ACCESS),
    ("files", "Files", "/files", FILES_VIEW),
    ("clients", "\U0001F465 Clients", "/clients", CLIENTS_READ),
    ("products", "\U0001F4E6 Products", "/products", PRODUCTS_READ),
    ("raw_materials", "\U0001FAA8 Raw Materials", "/raw-materials", RAW_MATERIALS_READ),
    ("suppliers", "\U0001F69A Suppliers", "/suppliers", SUPPLIERS_READ),
    ("quotations", "\U0001F4DD Quotations", "/quotations", QUOTATIONS_READ),
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
