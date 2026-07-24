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


-- ============================================================
-- Business Domain Tables
-- ============================================================

-- Clients: Customer/Client master records
CREATE TABLE IF NOT EXISTS clients (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(254) NULL,
    phone VARCHAR(50) NULL,
    address TEXT NULL,
    gstin VARCHAR(20) NULL,
    contact_person VARCHAR(150) NULL,
    payment_terms VARCHAR(100) NULL,
    credit_limit DECIMAL(14,2) NOT NULL DEFAULT 0,
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    notes TEXT NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Client/Customer master records';

-- Products: Finished goods product definitions
CREATE TABLE IF NOT EXISTS products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100) NULL,
    description TEXT NULL,
    default_bag_size_kg DECIMAL(10,3) NOT NULL DEFAULT 50,
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Product definitions';

-- Raw Materials: Raw material definitions
CREATE TABLE IF NOT EXISTS raw_materials (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL DEFAULT 'kg',
    description TEXT NULL,
    supplier_id BIGINT NULL,
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Raw material definitions';

-- Formulas: Bill of Materials (BOM) - product composition
CREATE TABLE IF NOT EXISTS formulas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    material_id BIGINT NOT NULL,
    percentage DECIMAL(8,4) NOT NULL,
    notes TEXT NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    UNIQUE KEY uq_formula_line (product_id, material_id),
    CONSTRAINT fk_formula_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_formula_material FOREIGN KEY (material_id) REFERENCES raw_materials(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_material_id (material_id),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Product formulas (Bill of Materials)';

-- Suppliers: Supplier master records
CREATE TABLE IF NOT EXISTS suppliers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    contact_person VARCHAR(150) NULL,
    phone VARCHAR(50) NULL,
    email VARCHAR(254) NULL,
    address TEXT NULL,
    gstin VARCHAR(20) NULL,
    category VARCHAR(100) NULL,
    rating TINYINT NULL,
    payment_terms VARCHAR(100) NULL,
    delivery_cost DECIMAL(12,2) NOT NULL DEFAULT 0,
    status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
    notes TEXT NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Supplier master records';

-- Quotations: Client quotations. quotations.create and quotations.approve
-- are restricted by role via QUOTATION_CREATOR_ROLE / QUOTATION_APPROVER_ROLE
-- in .env - see backend/app/permissions/definitions.py.
CREATE TABLE IF NOT EXISTS quotations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    quotation_no VARCHAR(50) NOT NULL UNIQUE,
    client_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity_kg DECIMAL(14,3) NOT NULL,
    bag_size_kg DECIMAL(10,3) NOT NULL DEFAULT 50,
    bags INT NOT NULL DEFAULT 0,
    valid_until DATE NULL,
    status ENUM('Draft','Pending','Approved','Rejected','Expired') NOT NULL DEFAULT 'Draft',
    priority ENUM('Critical','High','Normal','Low') NOT NULL DEFAULT 'Normal',
    notes TEXT NULL,
    approved_by VARCHAR(64) NULL,
    approved_at DATETIME(6) NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_quotation_client FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE RESTRICT,
    CONSTRAINT fk_quotation_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_client_id (client_id),
    INDEX idx_product_id (product_id),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Client quotations, role-gated creation and approval';

-- Orders: created only from Approved quotations, via
-- POST /api/quotations/convert-approved-to-orders (see CRUD_API.md).
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(50) NOT NULL UNIQUE,
    quotation_id BIGINT NOT NULL UNIQUE,
    client_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity_kg DECIMAL(14,3) NOT NULL,
    bag_size_kg DECIMAL(10,3) NOT NULL DEFAULT 50,
    bags INT NOT NULL DEFAULT 0,
    delivery_date DATE NULL,
    status ENUM('Pending','Confirmed','In Production','Ready','Shipped','Closed','Cancelled') NOT NULL DEFAULT 'Pending',
    priority ENUM('Critical','High','Normal','Low') NOT NULL DEFAULT 'Normal',
    notes TEXT NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_order_quotation FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE RESTRICT,
    CONSTRAINT fk_order_client FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE RESTRICT,
    CONSTRAINT fk_order_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_client_id (client_id),
    INDEX idx_product_id (product_id),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Orders, created only by converting an Approved quotation';
