-- ABC Enterprises reference application - test/demo data.
--
-- This seeds ONLY the perennia-access side: the application's permission
-- vocabulary and the three demo roles, exactly matching
-- backend/app/permissions/definitions.py. That module seeds the same data
-- idempotently every time the backend starts, so running this file is
-- optional - it exists for people who want to inspect or load the data
-- with a SQL client instead of running the app.
--
-- If you change backend/app/permissions/definitions.py, update this file
-- to match; it is not generated automatically.
--
-- What this file deliberately does NOT contain: any perennia-auth data
-- (no auth_subjects / auth_passwords rows). Login-ready demo accounts
-- need a real password hash produced by perennia-auth's own hashing
-- code - that can't be hand-written as SQL without reimplementing
-- authentication, which this application does not do. For accounts you
-- can actually sign in with, run:
--
--     python backend/scripts/seed_demo_data.py
--
-- Apply this file with:
--     mysql -u <user> -p <database> < backend/sql/test_data.sql
-- after backend/sql/schema.sql (or backend/scripts/init_db.py) has been applied.

INSERT INTO permissions (code, description) VALUES
    ('profile.view', 'View your own profile page'),
    ('reports.view', 'View the reports area'),
    ('admin.access', 'Access the administration area')
ON DUPLICATE KEY UPDATE description = VALUES(description);

INSERT INTO roles (code, description) VALUES
    ('employee', 'Standard ABC Enterprises employee'),
    ('manager', 'Team manager with reporting access'),
    ('administrator', 'Full administrative access')
ON DUPLICATE KEY UPDATE description = VALUES(description);

-- employee: profile.view
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.code = 'employee' AND p.code = 'profile.view'
ON DUPLICATE KEY UPDATE assigned_at = role_permissions.assigned_at;

-- manager: profile.view, reports.view
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.code = 'manager' AND p.code IN ('profile.view', 'reports.view')
ON DUPLICATE KEY UPDATE assigned_at = role_permissions.assigned_at;

-- administrator: profile.view, reports.view, admin.access
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.code = 'administrator' AND p.code IN ('profile.view', 'reports.view', 'admin.access')
ON DUPLICATE KEY UPDATE assigned_at = role_permissions.assigned_at;
