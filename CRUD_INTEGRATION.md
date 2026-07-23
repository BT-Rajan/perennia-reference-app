# CRUD Integration Guide

Quick start guide for integrating and using the perennia-crud CRUD system for business domain entities.

## Quick Start (5 minutes)

### 1. Database Setup
```bash
# Apply schema
mysql -u root -p abc_enterprises < backend/sql/schema.sql

# Load seed data (optional)
mysql -u root -p abc_enterprises < backend/sql/seed_crud_data.sql
```

### 2. Run Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Test API
```bash
# Get auth token (see perennia-auth docs)
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# List clients
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/clients

# Create client
curl -X POST http://localhost:8000/api/clients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Client", "email": "test@example.com", "status": "Active"}'
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          FastAPI App                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              API Routes (crud.py, crud_bulk.py)            │ │
│  │  GET/POST /api/clients, /api/products, etc.               │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │           Dependency Injection (deps.py)                   │ │
│  │  - Authentication (perennia-auth)                          │ │
│  │  - Authorization (perennia-access)                         │ │
│  │  - CRUD Engines (6x CrudEngine instances)                  │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │           Entity Schemas (entities.py)                     │ │
│  │  - clients, products, raw_materials, formulas,            │ │
│  │    suppliers, orders                                       │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │          Business Logic Hooks (hooks.py)                   │ │
│  │  - Validation (before_create, before_update)              │ │
│  │  - Side effects (after_create, after_update)              │ │
│  │  - Audit logging (all operations)                         │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │    perennia-crud CrudEngine (6x instances)                 │ │
│  │  - Handles all CRUD operations                            │ │
│  │  - Enforces permissions via perennia-access              │ │
│  │  - Calls hooks at appropriate lifecycle points           │ │
│  │  - Manages soft deletes                                  │ │
│  └──────────────────────┬─────────────────────────────────────┘ │
│                         │                                         │
│  ┌──────────────────────▼─────────────────────────────────────┐ │
│  │              MySQL Database                                │ │
│  │  - clients, products, raw_materials, formulas,           │ │
│  │    suppliers, orders (with soft_delete support)         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Example: Create Client

```
1. POST /api/clients {"name": "Test", ...}
   │
2. FastAPI route (crud.py) validates request
   │
3. Extracts identity from JWT token (perennia-auth)
   │
4. Calls CrudEngine.create(data, identity)
   │
5. CrudEngine checks permission via perennia-access
   │ (requires "clients.create" permission)
   │
6. Calls ClientsHooks.before_create(data)
   │ - Validates: name required, credit_limit >= 0
   │ - Raises ValueError if validation fails
   │
7. Executes INSERT SQL (parameterized, safe from injection)
   │
8. Calls ClientsHooks.after_create(record)
   │ - Logs: "Client created: 1 - Test"
   │
9. Returns 201 with created record
```

---

## File Structure

```
perennia-reference-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          (existing)
│   │   │   ├── crud.py          ← NEW: Standard CRUD endpoints
│   │   │   ├── crud_bulk.py     ← NEW: Bulk operations
│   │   │   ├── home.py          (existing)
│   │   │   ├── profile.py       (existing)
│   │   │   ├── reports.py       (existing)
│   │   │   ├── administration.py (existing)
│   │   │   ├── search.py        (existing)
│   │   │   └── files.py         (existing)
│   │   ├── __init__.py
│   │   ├── entities.py          ← NEW: Entity schemas
│   │   ├── hooks.py             ← NEW: Business logic hooks
│   │   ├── main.py              (MODIFIED: added CRUD routers)
│   │   ├── deps.py              (MODIFIED: added CRUD engines)
│   │   ├── config/
│   │   │   ├── errors.py        (existing)
│   │   │   └── settings.py      (existing)
│   │   ├── models/              (existing)
│   │   ├── permissions/
│   │   │   └── definitions.py   (MODIFIED: added CRUD permissions)
│   │   └── ...
│   ├── pyproject.toml
│   ├── sql/
│   │   ├── schema.sql           (MODIFIED: added CRUD tables)
│   │   ├── test_data.sql        (existing)
│   │   └── seed_crud_data.sql   ← NEW: Development seed data
│   └── scripts/
├── frontend/                     (existing)
├── CRUD_API.md                  ← NEW: Comprehensive API docs
├── CRUD_INTEGRATION.md          ← NEW: This file
├── README.md                     (existing)
└── ...
```

---

## Entity Relationships

```
Clients (👥)
  └─ Orders (📋)
     ├─ Product (📦)
     │  └─ Formulas (🧪)
     │     └─ Raw Materials (🪨)
     │        └─ Suppliers (🚚)
     └─ Client (👥)
```

### Database Relationships
```sql
-- Foreign Keys
orders.client_id -> clients.id (RESTRICT)
orders.product_id -> products.id (RESTRICT)
formulas.product_id -> products.id (CASCADE)
formulas.material_id -> raw_materials.id (CASCADE)
suppliers.name <- raw_materials.supplier_id (optional)
```

---

## Adding a New Entity (Template)

To add a new entity (e.g., Invoices):

### 1. Create Table (backend/sql/schema.sql)
```sql
CREATE TABLE IF NOT EXISTS invoices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    invoice_no VARCHAR(50) NOT NULL UNIQUE,
    client_id BIGINT NOT NULL,
    amount DECIMAL(14,2) NOT NULL,
    status ENUM('Draft','Sent','Paid','Overdue') NOT NULL DEFAULT 'Draft',
    notes TEXT NULL,
    deleted_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_invoice_client FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE RESTRICT,
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2. Define Entity Schema (app/entities.py)
```python
invoices = EntitySchema(
    table="invoices",
    fields=["invoice_no", "client_id", "amount", "status", "notes"],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="invoices"
)
```

### 3. Create Hooks (app/hooks.py)
```python
class InvoicesHooks:
    @staticmethod
    def before_create(data: dict) -> None:
        if not data.get("invoice_no"):
            raise ValueError("Invoice number required")
        if data.get("amount", 0) <= 0:
            raise ValueError("Amount must be positive")

    @staticmethod
    def after_create(record: dict) -> None:
        logger.info(f"Invoice created: {record['id']} - {record['invoice_no']}")
    
    # ... other hooks
```

### 4. Add CRUD Engine (app/deps.py)
```python
from app import entities, hooks

crud_invoices = CrudEngine(
    crud_config, entities.invoices,
    access=access,
    hooks=hooks.InvoicesHooks()
)
```

### 5. Create API Endpoints (app/api/crud.py)
```python
@router.get("/invoices")
def list_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    query = ListQuery(
        page=page,
        page_size=page_size,
        filters={"status": status} if status else {}
    )
    result = crud_invoices.list(query, identity=identity)
    return ListResponse(
        data=result.items,
        meta=ListResponseMeta(
            pagination=PaginationInfo(
                total=result.total,
                page=result.page,
                page_size=result.page_size
            )
        )
    )

# ... create, get, update, delete, restore endpoints
```

### 6. Add Permissions (app/permissions/definitions.py)
```python
INVOICES_CREATE = "invoices.create"
INVOICES_READ = "invoices.read"
INVOICES_UPDATE = "invoices.update"
INVOICES_DELETE = "invoices.delete"
INVOICES_RESTORE = "invoices.restore"

PERMISSIONS: list[tuple[str, str]] = [
    # ... existing permissions
    (INVOICES_CREATE, "Create invoices"),
    (INVOICES_READ, "View invoices"),
    # ... etc
]
```

### 7. Add Bulk Operations (app/api/crud_bulk.py)
```python
@router.post("/invoices/create")
def bulk_create_invoices(records: List[dict], identity: Identity = Depends(identity_required)):
    try:
        created = crud_invoices.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ... other bulk operations
```

**That's it!** The new entity now has:
- ✅ Full CRUD API endpoints
- ✅ Soft delete support
- ✅ Pagination and filtering
- ✅ Role-based access control
- ✅ Validation hooks
- ✅ Audit logging
- ✅ Bulk operations

---

## Testing

### Unit Tests
```python
# tests/test_crud.py
import pytest
from app.deps import crud_clients
from perennia_crud.exceptions import RecordNotFoundError

def test_create_client():
    data = {"name": "Test Client", "email": "test@example.com", "status": "Active"}
    record = crud_clients.create(data)
    assert record["id"] is not None
    assert record["name"] == "Test Client"

def test_client_validation():
    with pytest.raises(ValueError, match="Client name is required"):
        crud_clients.create({"email": "test@example.com"})

def test_soft_delete():
    record = crud_clients.create({"name": "Delete Me"})
    crud_clients.delete(record["id"])
    # Record is soft-deleted but still exists in DB
    assert crud_clients.get(record["id"], include_deleted=True) is not None

def test_restore():
    record = crud_clients.create({"name": "Delete Me"})
    crud_clients.delete(record["id"])
    restored = crud_clients.restore(record["id"])
    assert restored["deleted_at"] is None
```

### Integration Tests
```bash
# Run with pytest
pytest backend/tests/

# With coverage
pytest --cov=backend/app backend/tests/

# Specific test
pytest backend/tests/test_crud.py::test_create_client
```

### API Tests (curl)
```bash
# Set up
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -d '{"email":"admin@example.com","password":"password"}' \
  | jq -r '.token')

# Create
CLIENT_ID=$(curl -X POST http://localhost:8000/api/clients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","status":"Active"}' \
  | jq -r '.data.id')

# Read
curl http://localhost:8000/api/clients/$CLIENT_ID \
  -H "Authorization: Bearer $TOKEN"

# Update
curl -X PUT http://localhost:8000/api/clients/$CLIENT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"Inactive"}'

# Delete
curl -X DELETE http://localhost:8000/api/clients/$CLIENT_ID \
  -H "Authorization: Bearer $TOKEN"

# Restore
curl -X POST http://localhost:8000/api/clients/$CLIENT_ID/restore \
  -H "Authorization: Bearer $TOKEN"
```

---

## Performance Optimization

### Database Indexes
All entity tables have indexes on:
- `status` - for filtering by status
- `deleted_at` - for soft delete filtering
- Foreign keys - for joins
- Unique fields - for uniqueness constraints

### Query Optimization
```python
# Good - uses indexed fields
list_query = ListQuery(
    filters={"status": "Active"}  # Indexed
)

# Also good - pagination
list_query = ListQuery(
    page=1, page_size=20  # Uses OFFSET/LIMIT
)

# Avoid N+1 queries - bulk operations
crud_clients.bulk_create(records)  # One batch insert
crud_clients.bulk_update(updates)  # One batch update
```

### Connection Pooling
perennia-crud manages connection pooling automatically. Configure in `CrudDatabaseConfig`:
```python
CrudDatabaseConfig(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="abc_enterprises",
    # Additional settings:
    # pool_size=5,
    # max_overflow=10,
    # pool_recycle=3600,
)
```

---

## Deployment Checklist

- [ ] Database created and schema applied
- [ ] Seed data loaded (optional)
- [ ] Environment variables configured:
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
  - `AUTH_SIGNING_SECRET`
  - `CORS_ORIGINS`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (if applicable)
- [ ] Permission definitions seeded
- [ ] HTTPS enabled (production)
- [ ] Rate limiting configured (optional)
- [ ] Logging configured
- [ ] Backups configured
- [ ] Monitoring set up

---

## Troubleshooting

### "Record not found"
```python
# Check if record exists
try:
    record = crud_clients.get(1)
except RecordNotFoundError:
    print("Record doesn't exist or is soft-deleted")

# Include deleted records
record = crud_clients.get(1, include_deleted=True)
```

### "Permission denied" (403)
```python
# Check user's permissions
access.get_subject_permissions(subject_id)

# Assign permission to role
access.assign_permission_to_role("manager", "clients.create")

# Verify assignment
access.has_permission(identity, "clients.create")
```

### "Validation error"
```python
# Hooks validate before insert
# Check hook implementation in hooks.py
# Error message comes from hook's ValueError
```

### Slow queries
```python
# Check database indexes
SHOW INDEX FROM clients;

# Analyze query performance
EXPLAIN SELECT * FROM clients WHERE status = 'Active';

# Monitor slow query log
mysql> SET GLOBAL slow_query_log = 'ON';
```

---

## Resources

- **API Documentation**: See `CRUD_API.md` for full endpoint reference
- **perennia-crud**: https://github.com/BT-Rajan/perennia-crud
- **perennia-auth**: https://github.com/BT-Rajan/perennia-auth
- **perennia-access**: https://github.com/BT-Rajan/perennia-access
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/

---

## Support

For issues or questions:
1. Check `CRUD_API.md` for API reference
2. Review `hooks.py` for validation rules
3. Check application logs for error details
4. Refer to perennia-crud documentation
5. Open an issue on GitHub

---

**Last Updated**: 2024-01-20
**Version**: 1.0.0
**Status**: Production Ready ✅
