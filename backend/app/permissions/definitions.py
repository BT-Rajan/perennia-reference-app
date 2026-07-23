"""
Central permission vocabulary for ABC Enterprises.

This is the ONLY place application permission codes are declared.
perennia-access owns roles, permissions, and the authorization decision
itself; this module only owns the application's *vocabulary* (which
permissions exist, and which demo roles grant which permissions) and
seeds that vocabulary into perennia-access on startup.

Nothing in this application checks a role name to make an authorization
decision (e.g. `if role == "Administrator"`). Every protected route
checks a permission code through perennia-access - see app/deps.py.
"""
from perennia_access import PerenniaAccess

PROFILE_VIEW = "profile.view"
REPORTS_VIEW = "reports.view"
ADMIN_ACCESS = "admin.access"

# Search permissions (perennia-search integration)
SEARCH_ACCESS = "search.execute"
SEARCH_MANAGE = "search.manage"

# File storage permissions (perennia-files integration)
FILES_UPLOAD = "file.upload"
FILES_VIEW = "file.view"
FILES_MANAGE = "file.manage"

# ─── Clients Entity Permissions
CLIENTS_CREATE = "clients.create"
CLIENTS_READ = "clients.read"
CLIENTS_UPDATE = "clients.update"
CLIENTS_DELETE = "clients.delete"
CLIENTS_RESTORE = "clients.restore"

# ─── Products Entity Permissions
PRODUCTS_CREATE = "products.create"
PRODUCTS_READ = "products.read"
PRODUCTS_UPDATE = "products.update"
PRODUCTS_DELETE = "products.delete"
PRODUCTS_RESTORE = "products.restore"

# ─── Raw Materials Entity Permissions
RAW_MATERIALS_CREATE = "raw_materials.create"
RAW_MATERIALS_READ = "raw_materials.read"
RAW_MATERIALS_UPDATE = "raw_materials.update"
RAW_MATERIALS_DELETE = "raw_materials.delete"
RAW_MATERIALS_RESTORE = "raw_materials.restore"

# ─── Formulas Entity Permissions
FORMULAS_CREATE = "formulas.create"
FORMULAS_READ = "formulas.read"
FORMULAS_UPDATE = "formulas.update"
FORMULAS_DELETE = "formulas.delete"
FORMULAS_RESTORE = "formulas.restore"

# ─── Suppliers Entity Permissions
SUPPLIERS_CREATE = "suppliers.create"
SUPPLIERS_READ = "suppliers.read"
SUPPLIERS_UPDATE = "suppliers.update"
SUPPLIERS_DELETE = "suppliers.delete"
SUPPLIERS_RESTORE = "suppliers.restore"

# ─── Quotations Entity Permissions
# quotations.create and quotations.approve are NOT granted through the
# ROLES table below - they are granted exclusively to the roles named by
# QUOTATION_CREATOR_ROLE / QUOTATION_APPROVER_ROLE in .env, at the bottom
# of seed(). Every other quotations permission follows the normal pattern.
QUOTATIONS_CREATE = "quotations.create"
QUOTATIONS_READ = "quotations.read"
QUOTATIONS_UPDATE = "quotations.update"
QUOTATIONS_DELETE = "quotations.delete"
QUOTATIONS_RESTORE = "quotations.restore"
QUOTATIONS_APPROVE = "quotations.approve"

PERMISSIONS: list[tuple[str, str]] = [
    (PROFILE_VIEW, "View your own profile page"),
    (REPORTS_VIEW, "View the reports area"),
    (ADMIN_ACCESS, "Access the administration area"),
    (SEARCH_ACCESS, "Search across business resources"),
    (SEARCH_MANAGE, "Manage search indexes and configuration"),
    (FILES_UPLOAD, "Upload files to secure storage"),
    (FILES_VIEW, "Download and view files"),
    (FILES_MANAGE, "Manage files (versions, deletion, restoration)"),
    (CLIENTS_CREATE, "Create clients"),
    (CLIENTS_READ, "View clients"),
    (CLIENTS_UPDATE, "Update clients"),
    (CLIENTS_DELETE, "Delete clients"),
    (CLIENTS_RESTORE, "Restore clients"),
    (PRODUCTS_CREATE, "Create products"),
    (PRODUCTS_READ, "View products"),
    (PRODUCTS_UPDATE, "Update products"),
    (PRODUCTS_DELETE, "Delete products"),
    (PRODUCTS_RESTORE, "Restore products"),
    (RAW_MATERIALS_CREATE, "Create raw materials"),
    (RAW_MATERIALS_READ, "View raw materials"),
    (RAW_MATERIALS_UPDATE, "Update raw materials"),
    (RAW_MATERIALS_DELETE, "Delete raw materials"),
    (RAW_MATERIALS_RESTORE, "Restore raw materials"),
    (FORMULAS_CREATE, "Create formulas"),
    (FORMULAS_READ, "View formulas"),
    (FORMULAS_UPDATE, "Update formulas"),
    (FORMULAS_DELETE, "Delete formulas"),
    (FORMULAS_RESTORE, "Restore formulas"),
    (SUPPLIERS_CREATE, "Create suppliers"),
    (SUPPLIERS_READ, "View suppliers"),
    (SUPPLIERS_UPDATE, "Update suppliers"),
    (SUPPLIERS_DELETE, "Delete suppliers"),
    (SUPPLIERS_RESTORE, "Restore suppliers"),
    (QUOTATIONS_CREATE, "Create quotations"),
    (QUOTATIONS_READ, "View quotations"),
    (QUOTATIONS_UPDATE, "Update quotations"),
    (QUOTATIONS_DELETE, "Delete quotations"),
    (QUOTATIONS_RESTORE, "Restore quotations"),
    (QUOTATIONS_APPROVE, "Approve quotations"),
]

# Demo application roles and the permissions each one carries.
# These are application data managed through perennia-access - not
# hardcoded authorization logic.
ROLES: dict[str, dict] = {
    "employee": {
        "description": "Standard ABC Enterprises employee",
        "permissions": [
            PROFILE_VIEW, SEARCH_ACCESS, FILES_VIEW,
            # Read-only access to all CRUD entities
            CLIENTS_READ, PRODUCTS_READ, RAW_MATERIALS_READ,
            FORMULAS_READ, SUPPLIERS_READ, QUOTATIONS_READ,
        ],
    },
    "manager": {
        "description": "Team manager with reporting access",
        "permissions": [
            PROFILE_VIEW, REPORTS_VIEW, SEARCH_ACCESS, SEARCH_MANAGE,
            FILES_UPLOAD, FILES_VIEW, FILES_MANAGE,
            # Full CRUD access to all business entities
            CLIENTS_CREATE, CLIENTS_READ, CLIENTS_UPDATE, CLIENTS_DELETE, CLIENTS_RESTORE,
            PRODUCTS_CREATE, PRODUCTS_READ, PRODUCTS_UPDATE, PRODUCTS_DELETE, PRODUCTS_RESTORE,
            RAW_MATERIALS_CREATE, RAW_MATERIALS_READ, RAW_MATERIALS_UPDATE, RAW_MATERIALS_DELETE, RAW_MATERIALS_RESTORE,
            FORMULAS_CREATE, FORMULAS_READ, FORMULAS_UPDATE, FORMULAS_DELETE, FORMULAS_RESTORE,
            SUPPLIERS_CREATE, SUPPLIERS_READ, SUPPLIERS_UPDATE, SUPPLIERS_DELETE, SUPPLIERS_RESTORE,
            # quotations.create is granted separately below, to QUOTATION_CREATOR_ROLE only
            QUOTATIONS_READ, QUOTATIONS_UPDATE, QUOTATIONS_DELETE, QUOTATIONS_RESTORE,
        ],
    },
    "administrator": {
        "description": "Full administrative access",
        "permissions": [
            PROFILE_VIEW, REPORTS_VIEW, ADMIN_ACCESS, SEARCH_ACCESS, SEARCH_MANAGE,
            FILES_UPLOAD, FILES_VIEW, FILES_MANAGE,
            # Full CRUD access to all business entities
            CLIENTS_CREATE, CLIENTS_READ, CLIENTS_UPDATE, CLIENTS_DELETE, CLIENTS_RESTORE,
            PRODUCTS_CREATE, PRODUCTS_READ, PRODUCTS_UPDATE, PRODUCTS_DELETE, PRODUCTS_RESTORE,
            RAW_MATERIALS_CREATE, RAW_MATERIALS_READ, RAW_MATERIALS_UPDATE, RAW_MATERIALS_DELETE, RAW_MATERIALS_RESTORE,
            FORMULAS_CREATE, FORMULAS_READ, FORMULAS_UPDATE, FORMULAS_DELETE, FORMULAS_RESTORE,
            SUPPLIERS_CREATE, SUPPLIERS_READ, SUPPLIERS_UPDATE, SUPPLIERS_DELETE, SUPPLIERS_RESTORE,
            # quotations.create is granted separately below, to QUOTATION_CREATOR_ROLE only
            QUOTATIONS_READ, QUOTATIONS_UPDATE, QUOTATIONS_DELETE, QUOTATIONS_RESTORE,
        ],
    },
}

# Roles offered on the registration form, in display order.
REGISTERABLE_ROLES: list[tuple[str, str]] = [
    ("employee", "Employee"),
    ("manager", "Manager"),
    ("administrator", "Administrator"),
]


def seed(access: PerenniaAccess, settings) -> None:
    """Idempotently ensure the application's permissions and demo roles
    exist in perennia-access. Safe to call on every startup.

    `settings` supplies QUOTATION_CREATOR_ROLE / QUOTATION_APPROVER_ROLE
    (see app.config.settings). quotations.create and quotations.approve are
    granted ONLY to those two roles - and unassigned from every other role -
    so changing the .env value and restarting is enough to move who can
    create or approve quotations, without touching this file.
    """
    for code, description in PERMISSIONS:
        if access.get_permission(code) is None:
            access.create_permission(code, description)

    for role_code, role_def in ROLES.items():
        if access.get_role(role_code) is None:
            access.create_role(role_code, role_def["description"])

        existing = set(access.get_role_permissions(role_code))
        for perm_code in role_def["permissions"]:
            if perm_code not in existing:
                access.assign_permission_to_role(role_code, perm_code)

    creator_role = settings.quotation_creator_role
    approver_role = settings.quotation_approver_role
    for role_code in (creator_role, approver_role):
        if access.get_role(role_code) is None:
            raise RuntimeError(
                f"QUOTATION_CREATOR_ROLE/QUOTATION_APPROVER_ROLE names role "
                f"'{role_code}', which does not exist. Valid roles: "
                f"{', '.join(ROLES.keys())}."
            )

    for role_code in ROLES.keys():
        held = set(access.get_role_permissions(role_code))

        should_create = role_code == creator_role
        has_create = QUOTATIONS_CREATE in held
        if should_create and not has_create:
            access.assign_permission_to_role(role_code, QUOTATIONS_CREATE)
        elif not should_create and has_create:
            access.unassign_permission_from_role(role_code, QUOTATIONS_CREATE)

        should_approve = role_code == approver_role
        has_approve = QUOTATIONS_APPROVE in held
        if should_approve and not has_approve:
            access.assign_permission_to_role(role_code, QUOTATIONS_APPROVE)
        elif not should_approve and has_approve:
            access.unassign_permission_from_role(role_code, QUOTATIONS_APPROVE)

        # The creator role needs quotations.read too: CrudEngine.create()
        # re-fetches the record it just inserted before returning it.
        if should_create and QUOTATIONS_READ not in held:
            access.assign_permission_to_role(role_code, QUOTATIONS_READ)
        # The approver role needs quotations.update: the approve endpoint
        # goes through CrudEngine.update() to persist the status change.
        if should_approve and QUOTATIONS_UPDATE not in held:
            access.assign_permission_to_role(role_code, QUOTATIONS_UPDATE)
