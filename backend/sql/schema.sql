-- ABC Enterprises reference application - combined database schema.
--
-- GENERATED FILE - do not hand-edit.
-- Produced by backend/scripts/generate_schema_sql.py, which exports the
-- schema.sql shipped inside the installed perennia-auth and
-- perennia-access packages, unmodified. Re-run that script after
-- upgrading either dependency instead of editing this file directly.
-- perennia-auth   version: 1.0.0
-- perennia-access version: 1.0.0
--
-- Apply with: mysql -u <user> -p <database> < backend/sql/schema.sql
-- (equivalent to running backend/scripts/init_db.py)


-- ============================================================
-- perennia-auth 1.0.0 (source: https://github.com/BT-Rajan/perennia-auth)
-- ============================================================
CREATE TABLE IF NOT EXISTS auth_subjects (
    id            CHAR(36)     NOT NULL PRIMARY KEY,
    status        ENUM('pending','active','locked','suspended','disabled','deleted')
                  NOT NULL DEFAULT 'pending',
    locked_until  DATETIME(6)  NULL,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                  ON UPDATE CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_identifiers (
    id            CHAR(36)     NOT NULL PRIMARY KEY,
    subject_id    CHAR(36)     NOT NULL,
    email         VARCHAR(254) NOT NULL,
    is_verified   TINYINT(1)   NOT NULL DEFAULT 0,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                  ON UPDATE CURRENT_TIMESTAMP(6),
    UNIQUE KEY uq_auth_identifiers_email (email),
    KEY idx_auth_identifiers_subject (subject_id),
    CONSTRAINT fk_identifiers_subject FOREIGN KEY (subject_id)
        REFERENCES auth_subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_passwords (
    subject_id    CHAR(36)     NOT NULL PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                  ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_passwords_subject FOREIGN KEY (subject_id)
        REFERENCES auth_subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_sessions (
    id                CHAR(36)    NOT NULL PRIMARY KEY,
    subject_id        CHAR(36)    NOT NULL,
    status            ENUM('active','expired','revoked') NOT NULL DEFAULT 'active',
    created_at        DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    last_activity_at  DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    expires_at        DATETIME(6) NOT NULL,
    revoked_at        DATETIME(6) NULL,
    ip_address        VARCHAR(45) NULL,
    user_agent        VARCHAR(512) NULL,
    KEY idx_auth_sessions_subject (subject_id),
    CONSTRAINT fk_sessions_subject FOREIGN KEY (subject_id)
        REFERENCES auth_subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_refresh_tokens (
    id            CHAR(36)     NOT NULL PRIMARY KEY,
    session_id    CHAR(36)     NOT NULL,
    token_hash    CHAR(64)     NOT NULL,
    expires_at    DATETIME(6)  NOT NULL,
    used_at       DATETIME(6)  NULL,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    UNIQUE KEY uq_refresh_token_hash (token_hash),
    KEY idx_refresh_session (session_id),
    CONSTRAINT fk_refresh_session FOREIGN KEY (session_id)
        REFERENCES auth_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_verification_tokens (
    id            CHAR(36)     NOT NULL PRIMARY KEY,
    subject_id    CHAR(36)     NOT NULL,
    purpose       ENUM('email_verification','email_change','password_recovery') NOT NULL,
    token_hash    CHAR(64)     NOT NULL,
    metadata      JSON         NULL,
    expires_at    DATETIME(6)  NOT NULL,
    used_at       DATETIME(6)  NULL,
    attempt_count INT UNSIGNED NOT NULL DEFAULT 0,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    UNIQUE KEY uq_verification_token_hash (token_hash),
    KEY idx_verification_subject_purpose (subject_id, purpose),
    CONSTRAINT fk_verification_subject FOREIGN KEY (subject_id)
        REFERENCES auth_subjects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_failed_attempts (
    id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email         VARCHAR(254) NOT NULL,
    ip_address    VARCHAR(45)  NULL,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    KEY idx_failed_attempts_email_time (email, created_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS auth_security_events (
    id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    subject_id    CHAR(36)     NULL,
    event_type    VARCHAR(64)  NOT NULL,
    ip_address    VARCHAR(45)  NULL,
    user_agent    VARCHAR(512) NULL,
    metadata      JSON         NULL,
    created_at    DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    KEY idx_security_events_subject (subject_id),
    KEY idx_security_events_type (event_type)
) ENGINE=InnoDB;


-- ============================================================
-- perennia-access 1.0.0 (source: https://github.com/BT-Rajan/perennia-access)
-- ============================================================
-- perennia-access database schema
-- Run this once against your MySQL database

-- Permissions: application-defined permissions
CREATE TABLE IF NOT EXISTS permissions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(255) NOT NULL UNIQUE COMMENT 'e.g., customer.view, invoice.approve',
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Application permissions';

-- Roles: collections of permissions
CREATE TABLE IF NOT EXISTS roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(255) NOT NULL UNIQUE COMMENT 'e.g., admin, accountant',
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Authorization roles';

-- Role-Permission assignments: which permissions belong to which roles
CREATE TABLE IF NOT EXISTS role_permissions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_role_permission (role_id, permission_id),
    CONSTRAINT fk_role_permissions_role_id FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    CONSTRAINT fk_role_permissions_permission_id FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    INDEX idx_role_id (role_id),
    INDEX idx_permission_id (permission_id),
    INDEX idx_assigned_at (assigned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Assignment of permissions to roles';

-- User-Role assignments: which roles are assigned to which users (subjects)
CREATE TABLE IF NOT EXISTS user_roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    subject_id VARCHAR(255) NOT NULL COMMENT 'Subject ID from perennia-auth',
    role_id BIGINT NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_role (subject_id, role_id),
    CONSTRAINT fk_user_roles_role_id FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    INDEX idx_subject_id (subject_id),
    INDEX idx_role_id (role_id),
    INDEX idx_assigned_at (assigned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Assignment of roles to users (subjects from perennia-auth)';
