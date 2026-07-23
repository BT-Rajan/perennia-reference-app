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

PERMISSIONS: list[tuple[str, str]] = [
    (PROFILE_VIEW, "View your own profile page"),
    (REPORTS_VIEW, "View the reports area"),
    (ADMIN_ACCESS, "Access the administration area"),
    (SEARCH_ACCESS, "Search across business resources"),
    (SEARCH_MANAGE, "Manage search indexes and configuration"),
    (FILES_UPLOAD, "Upload files to secure storage"),
    (FILES_VIEW, "Download and view files"),
    (FILES_MANAGE, "Manage files (versions, deletion, restoration)"),
]

# Demo application roles and the permissions each one carries.
# These are application data managed through perennia-access - not
# hardcoded authorization logic.
ROLES: dict[str, dict] = {
    "employee": {
        "description": "Standard ABC Enterprises employee",
        "permissions": [PROFILE_VIEW, SEARCH_ACCESS, FILES_VIEW],
    },
    "manager": {
        "description": "Team manager with reporting access",
        "permissions": [PROFILE_VIEW, REPORTS_VIEW, SEARCH_ACCESS, SEARCH_MANAGE, FILES_UPLOAD, FILES_VIEW, FILES_MANAGE],
    },
    "administrator": {
        "description": "Full administrative access",
        "permissions": [PROFILE_VIEW, REPORTS_VIEW, ADMIN_ACCESS, SEARCH_ACCESS, SEARCH_MANAGE, FILES_UPLOAD, FILES_VIEW, FILES_MANAGE],
    },
}

# Roles offered on the registration form, in display order.
REGISTERABLE_ROLES: list[tuple[str, str]] = [
    ("employee", "Employee"),
    ("manager", "Manager"),
    ("administrator", "Administrator"),
]


def seed(access: PerenniaAccess) -> None:
    """Idempotently ensure the application's permissions and demo roles
    exist in perennia-access. Safe to call on every startup.
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
