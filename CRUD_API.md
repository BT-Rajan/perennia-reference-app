# CRUD API Documentation

Comprehensive CRUD (Create, Read, Update, Delete) operations for all business domain entities using **perennia-crud**, a lightweight, reusable CRUD engine.

## Overview

This API provides standardized CRUD endpoints for:
- **👥 Clients** - Customer/client master records
- **📦 Products** - Finished goods definitions
- **🪨 Raw Materials** - Raw material definitions
- **🧪 Formulas** - Bill of Materials (product composition)
- **🚚 Suppliers** - Supplier master records
- **🧾 Quotations** - Client quotations (role-gated creation & approval)

## Architecture

### Technology Stack
- **Framework**: FastAPI
- **CRUD Engine**: perennia-crud (single engine instance per entity)
- **Authentication**: perennia-auth (JWT-based)
- **Authorization**: perennia-access (role-based)
- **Database**: MySQL 8.0+ with soft-delete support

### Key Features
- ✅ Soft deletes (data marked deleted, not removed)
- ✅ Pagination and filtering
- ✅ Role-based access control (RBAC)
- ✅ Business logic hooks (validation, side effects)
- ✅ Bulk operations (create, update, delete, restore)
- ✅ Comprehensive error handling
- ✅ Audit-friendly (soft deletes, timestamps)

## Authentication & Authorization

### Required Headers
All requests require:
```
Authorization: Bearer <JWT_TOKEN>
```

### Permission Model
Each entity has 5 operations:
- `{entity}.create` - Create records
- `{entity}.read` - View records
- `{entity}.update` - Modify records
- `{entity}.delete` - Soft delete records
- `{entity}.restore` - Restore soft-deleted records

Quotations additionally have a 6th operation, `quotations.approve`, used only
by `POST /api/quotations/{id}/approve`.

### Default Roles
- **Employee**: Read-only access to all entities
- **Manager**: Full CRUD on all entities except quotations (read/update/delete/restore only)
- **Administrator**: Full CRUD + system management, except quotations (read/update/delete/restore only)

### Quotations: Role-Gated Creation & Approval
Unlike every other entity, `quotations.create` and `quotations.approve` are
**not** assigned through the roles above. They are granted, exclusively, to
the two roles named in `.env`:

```
QUOTATION_CREATOR_ROLE=manager        # only this role can create quotations
QUOTATION_APPROVER_ROLE=administrator # only this role can approve quotations
```

At startup, `app/permissions/definitions.py:seed()` grants `quotations.create`
to whichever role `QUOTATION_CREATOR_ROLE` names and `quotations.approve` to
whichever role `QUOTATION_APPROVER_ROLE` names - and revokes those two
permissions from every other role. Changing either value in `.env` and
restarting the app is enough to move the restriction; no code change needed.
Both variables must name a role that exists (`employee`, `manager`, or
`administrator`), or the app will refuse to start.

A quotation can never be approved through the generic
`PUT /api/quotations/{id}` endpoint, even by an identity that holds
`quotations.update` - only `POST /api/quotations/{id}/approve` can set
status to `Approved`.

## API Endpoints

### Standard CRUD Endpoints

Each entity (clients, products, raw_materials, formulas, suppliers, quotations) supports:

#### List Records
```http
GET /api/{entity}?page=1&page_size=20&status=Active&search=query
```

**Query Parameters:**
- `page` (int, default=1): Page number
- `page_size` (int, default=20, max=100): Records per page
- `search` (string, optional): Full-text search
- `status` (string, optional): Filter by status
- Entity-specific filters (e.g., `client_id`, `product_id`)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Acme Manufacturing",
      "email": "contact@acme.com",
      "status": "Active",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "deleted_at": null
    }
  ],
  "meta": {
    "pagination": {
      "total": 47,
      "page": 1,
      "page_size": 20
    }
  }
}
```

#### Get Single Record
```http
GET /api/{entity}/{id}
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Acme Manufacturing",
    "email": "contact@acme.com",
    "status": "Active",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "deleted_at": null
  }
}
```

**Errors:**
- `404 Not Found` - Record doesn't exist

#### Create Record
```http
POST /api/{entity}
Content-Type: application/json

{
  "name": "New Client",
  "email": "new@client.com",
  "status": "Active",
  "notes": "Optional notes"
}
```

**Response:** (201 Created)
```json
{
  "data": {
    "id": 48,
    "name": "New Client",
    "email": "new@client.com",
    "status": "Active",
    "created_at": "2024-01-20T14:22:00Z",
    "updated_at": "2024-01-20T14:22:00Z",
    "deleted_at": null
  }
}
```

**Errors:**
- `400 Bad Request` - Validation failed
- `403 Forbidden` - Permission denied

#### Update Record
```http
PUT /api/{entity}/{id}
Content-Type: application/json

{
  "status": "Inactive",
  "notes": "Updated notes"
}
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Acme Manufacturing",
    "email": "contact@acme.com",
    "status": "Inactive",
    "updated_at": "2024-01-20T14:25:00Z",
    "deleted_at": null
  }
}
```

**Errors:**
- `404 Not Found` - Record doesn't exist
- `400 Bad Request` - Invalid update

#### Delete Record (Soft Delete)
```http
DELETE /api/{entity}/{id}
```

**Response:**
```json
{
  "success": true
}
```

**Note:** Records are soft-deleted (marked with `deleted_at` timestamp), not permanently removed.

#### Restore Record
```http
POST /api/{entity}/{id}/restore
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Acme Manufacturing",
    "deleted_at": null,
    "updated_at": "2024-01-20T14:30:00Z"
  }
}
```

---

## Bulk Operations

### Bulk Create
```http
POST /api/bulk/{entity}/create
Content-Type: application/json

[
  {"name": "Client 1", "email": "client1@test.com"},
  {"name": "Client 2", "email": "client2@test.com"},
  {"name": "Client 3", "email": "client3@test.com"}
]
```

**Response:**
```json
{
  "data": [
    {"id": 1, "name": "Client 1", ...},
    {"id": 2, "name": "Client 2", ...},
    {"id": 3, "name": "Client 3", ...}
  ],
  "count": 3
}
```

### Bulk Update
```http
POST /api/bulk/{entity}/update
Content-Type: application/json

[
  {"id": 1, "data": {"status": "Inactive"}},
  {"id": 2, "data": {"status": "Inactive"}},
  {"id": 3, "data": {"status": "Active"}}
]
```

**Response:**
```json
{
  "data": [
    {"id": 1, "status": "Inactive", ...},
    {"id": 2, "status": "Inactive", ...},
    {"id": 3, "status": "Active", ...}
  ],
  "count": 3
}
```

### Bulk Delete
```http
POST /api/bulk/{entity}/delete
Content-Type: application/json

[1, 2, 3]
```

**Response:**
```json
{
  "deleted": 3
}
```

### Bulk Restore
```http
POST /api/bulk/{entity}/restore
Content-Type: application/json

[1, 2, 3]
```

**Response:**
```json
{
  "data": [
    {"id": 1, "deleted_at": null, ...},
    {"id": 2, "deleted_at": null, ...},
    {"id": 3, "deleted_at": null, ...}
  ],
  "count": 3
}
```

---

## Entity-Specific Details

### 👥 Clients
**Table:** `clients`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment, read-only |
| name | VARCHAR(255) | ✓ | Unique client name |
| email | VARCHAR(254) | | Email address |
| phone | VARCHAR(50) | | Phone number |
| address | TEXT | | Full address |
| gstin | VARCHAR(20) | | GST ID (India) |
| contact_person | VARCHAR(150) | | Primary contact |
| payment_terms | VARCHAR(100) | | Net 30, Net 45, etc. |
| credit_limit | DECIMAL(14,2) | | Credit limit in currency |
| status | ENUM | ✓ | 'Active' or 'Inactive' |
| notes | TEXT | | Internal notes |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

**Validation:**
- Name is required
- Credit limit cannot be negative

### 📦 Products
**Table:** `products`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment |
| name | VARCHAR(255) | ✓ | Unique product name |
| category | VARCHAR(100) | | Product category |
| description | TEXT | | Product description |
| default_bag_size_kg | DECIMAL(10,3) | ✓ | Default bag size |
| status | ENUM | ✓ | 'Active' or 'Inactive' |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

**Validation:**
- Name is required
- Default bag size must be positive

### 🪨 Raw Materials
**Table:** `raw_materials`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment |
| name | VARCHAR(255) | ✓ | Unique material name |
| unit | VARCHAR(20) | ✓ | Unit (default: 'kg') |
| description | TEXT | | Material description |
| supplier_id | BIGINT | | Associated supplier |
| status | ENUM | ✓ | 'Active' or 'Inactive' |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

### 🧪 Formulas (Bill of Materials)
**Table:** `formulas`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment |
| product_id | BIGINT | ✓ | FK to products |
| material_id | BIGINT | ✓ | FK to raw_materials |
| percentage | DECIMAL(8,4) | ✓ | Material percentage (0-100) |
| notes | TEXT | | Formula notes |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

**Unique Constraint:** (product_id, material_id) - one formula line per material per product

**Validation:**
- Product ID required
- Material ID required
- Percentage must be 0-100

### 🚚 Suppliers
**Table:** `suppliers`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment |
| name | VARCHAR(255) | ✓ | Unique supplier name |
| contact_person | VARCHAR(150) | | Contact person name |
| phone | VARCHAR(50) | | Phone number |
| email | VARCHAR(254) | | Email address |
| address | TEXT | | Full address |
| gstin | VARCHAR(20) | | GST ID |
| category | VARCHAR(100) | | Supplier category |
| rating | TINYINT | | Rating (1-5) |
| payment_terms | VARCHAR(100) | | Payment terms |
| delivery_cost | DECIMAL(12,2) | | Delivery cost |
| status | ENUM | ✓ | 'Active' or 'Inactive' |
| notes | TEXT | | Internal notes |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

**Validation:**
- Name required
- Rating must be 1-5 (if provided)
- Delivery cost cannot be negative

### 🧾 Quotations
**Table:** `quotations`

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | BIGINT | ✓ | Auto-increment |
| quotation_no | VARCHAR(50) | ✓ | Unique quotation number |
| client_id | BIGINT | ✓ | FK to clients |
| product_id | BIGINT | ✓ | FK to products |
| quantity_kg | DECIMAL(14,3) | ✓ | Quantity in kg |
| bag_size_kg | DECIMAL(10,3) | ✓ | Bag size (default: 50) |
| bags | INT | ✓ | Number of bags |
| valid_until | DATE | | Quotation validity date |
| status | ENUM | ✓ | Draft, Pending, Approved, Rejected, Expired |
| priority | ENUM | ✓ | Critical, High, Normal, Low |
| notes | TEXT | | Quotation notes |
| approved_by | VARCHAR(64) | | Subject ID of the approving identity (set by the approve endpoint) |
| approved_at | DATETIME(6) | | Set by the approve endpoint |
| deleted_at | DATETIME(6) | | Soft delete timestamp |
| created_at | DATETIME(6) | ✓ | Auto-set |
| updated_at | DATETIME(6) | ✓ | Auto-updated |

**Validation:**
- Quotation number required
- Client ID required
- Product ID required
- Quantity must be positive
- Cannot modify client/product once a quotation leaves Draft/Pending
- Cannot delete an Approved quotation
- Cannot be created already Approved
- Cannot be moved to Approved through the generic update endpoint

**Creating a quotation** (`POST /api/quotations`) requires the
`quotations.create` permission, held only by the role named in
`QUOTATION_CREATOR_ROLE` (`.env`).

**Approving a quotation:**
```http
POST /api/quotations/{quotation_id}/approve
```
Requires the `quotations.approve` permission, held only by the role named in
`QUOTATION_APPROVER_ROLE` (`.env`). Sets `status` to `Approved`, and stamps
`approved_by` / `approved_at`. Returns `400` if the quotation is already
approved. This is the only way to approve a quotation - `PUT
/api/quotations/{quotation_id}` will reject any attempt to set
`status: "Approved"`.

---

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed"
  }
}
```

### Common Error Codes
| Code | Status | Meaning |
|------|--------|---------|
| `authentication_required` | 401 | Missing/invalid token |
| `permission_denied` | 403 | Permission check failed |
| `not_found` | 404 | Record not found |
| `validation_error` | 400 | Input validation failed |
| `conflict` | 409 | Business rule violation (e.g., duplicate name) |
| `internal_error` | 500 | Server error |

### Validation Errors
Each field error includes:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Client name is required"
  }
}
```

---

## Usage Examples

### Python (requests)
```python
import requests

BASE_URL = "http://localhost:8000/api"
HEADERS = {"Authorization": f"Bearer {token}"}

# List clients
response = requests.get(f"{BASE_URL}/clients?page=1&page_size=20", headers=HEADERS)
clients = response.json()["data"]

# Create client
new_client = {
    "name": "New Client Ltd",
    "email": "info@newclient.com",
    "status": "Active"
}
response = requests.post(f"{BASE_URL}/clients", json=new_client, headers=HEADERS)
client_id = response.json()["data"]["id"]

# Update client
updates = {"status": "Inactive"}
response = requests.put(f"{BASE_URL}/clients/{client_id}", json=updates, headers=HEADERS)

# Delete client
response = requests.delete(f"{BASE_URL}/clients/{client_id}", headers=HEADERS)

# Restore client
response = requests.post(f"{BASE_URL}/clients/{client_id}/restore", headers=HEADERS)
```

### JavaScript (fetch)
```javascript
const BASE_URL = "http://localhost:8000/api";
const headers = {"Authorization": `Bearer ${token}`};

// List clients
const response = await fetch(`${BASE_URL}/clients?page=1&page_size=20`, {headers});
const clients = (await response.json()).data;

// Create client
const newClient = {
  name: "New Client Ltd",
  email: "info@newclient.com",
  status: "Active"
};
const createResponse = await fetch(`${BASE_URL}/clients`, {
  method: "POST",
  headers: {...headers, "Content-Type": "application/json"},
  body: JSON.stringify(newClient)
});
const clientId = (await createResponse.json()).data.id;

// Update client
const updates = {status: "Inactive"};
await fetch(`${BASE_URL}/clients/${clientId}`, {
  method: "PUT",
  headers: {...headers, "Content-Type": "application/json"},
  body: JSON.stringify(updates)
});
```

---

## Deployment Checklist

- [ ] Database schema applied (`backend/sql/schema.sql`)
- [ ] Seed data loaded (optional: `backend/sql/seed_crud_data.sql`)
- [ ] perennia-crud dependency installed
- [ ] perennia-auth & perennia-access configured
- [ ] Permission definitions seeded on startup
- [ ] CORS configured for frontend origin
- [ ] JWT signing secret configured in environment
- [ ] Database credentials configured in environment
- [ ] Logging configured (INFO level recommended)
- [ ] HTTPS enabled in production

---

## Integration with Frontend

### React Example
```javascript
// useApi.js
export const useCrudApi = (entity) => {
  const [data, setData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const list = async (page = 1, filters = {}) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({page, ...filters});
      const response = await fetch(`/api/${entity}?${params}`, {
        headers: {"Authorization": `Bearer ${getToken()}`}
      });
      setData(await response.json());
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return {data, loading, error, list};
};

// Component usage
export const ClientsList = () => {
  const {data, loading, list} = useCrudApi("clients");

  React.useEffect(() => {
    list(1, {status: "Active"});
  }, []);

  return (
    <div>
      {loading && <p>Loading...</p>}
      {data?.data?.map(client => (
        <div key={client.id}>{client.name}</div>
      ))}
    </div>
  );
};
```

---

## Performance Considerations

- **Pagination**: Default 20 records/page, max 100
- **Indexes**: Automatic on status, created_at, deleted_at
- **Soft Deletes**: Queries automatically exclude deleted records
- **Bulk Operations**: Recommended for >10 records
- **Connection Pooling**: Configured in perennia-crud database config

---

## Support & Troubleshooting

### Common Issues

**401 Unauthorized**
- Verify token is valid and not expired
- Check `Authorization: Bearer <token>` format

**403 Forbidden**
- Verify user has required permission
- Check role assignments in perennia-access

**404 Not Found**
- Verify record ID exists and is not soft-deleted
- Use GET /api/{entity}/{id} to check

**400 Bad Request**
- Check validation errors in response
- Ensure all required fields are provided
- Verify field types match schema

---

For API details, see `/docs` (Swagger UI) or `/redoc` (ReDoc) after running the backend.
