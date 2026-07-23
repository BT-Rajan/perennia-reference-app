# Search and Files Integration Guide

This guide demonstrates how ABC Enterprises reference application integrates **perennia-search** and **perennia-files** for secure, scalable business resource management.

## Table of Contents

- [Overview](#overview)
- [Search Implementation](#search-implementation)
- [Files Implementation](#files-implementation)
- [Integration Points](#integration-points)
- [Usage Examples](#usage-examples)
- [Permission Model](#permission-model)

---

## Overview

### perennia-search

**perennia-search** provides full-text keyword search across registered business resources:

- **MySQL 8 FULLTEXT backed**: Efficient indexing and query performance
- **Multi-resource search**: Search customers, companies, documents, etc. in one query
- **Relevance scoring**: Results ranked by relevance to query keywords
- **Authorization integration**: Permission-based access control via perennia-access

### perennia-files

**perennia-files** enables secure file storage with versioning and AI processing:

- **Secure storage**: Encrypted file storage with signing and access control
- **Versioning**: Complete version history with immutable records
- **Soft deletion**: Retain deleted files for compliance with restore capability
- **Optional AI processing**: Extract text, summarize, ask questions, generate content

---

## Search Implementation

### Model Providers

The application registers three search providers demonstrating different entity types:

#### 1. **CustomerSearchProvider** (`app/models/search.py`)

Indexes customer records for discovery:

```python
from app.models.search import CustomerSearchProvider

provider = CustomerSearchProvider()

# List all indexed entities
customer_ids = provider.list_entity_ids()
# Returns: ['cust-001', 'cust-002', 'cust-003']

# Build searchable document
doc = provider.build_document('cust-001')
# Returns: ProviderDocument(
#     title="Acme Corporation",
#     content="Acme Corporation contact@acme.com +1-555-0100 Manufacturing",
#     metadata={"email": "contact@acme.com", "phone": "+1-555-0100", ...}
# )
```

#### 2. **CompanySearchProvider** (`app/models/search.py`)

Indexes company/partner information:

```python
from app.models.search import CompanySearchProvider

provider = CompanySearchProvider()

# Build document for a company
doc = provider.build_document('comp-001')
# Returns: ProviderDocument(
#     title="ABC Enterprises",
#     content="ABC Enterprises Leading provider of enterprise solutions...",
#     metadata={"headquarters": "New York, USA", "employees": "5000", ...}
# )
```

#### 3. **DocumentSearchProvider** (`app/models/search.py`)

Indexes document metadata and extracted content:

```python
from app.models.search import DocumentSearchProvider

provider = DocumentSearchProvider()

# Build document from file
doc = provider.build_document('doc-001')
# Returns: ProviderDocument(
#     title="Service Agreement 2024.pdf",
#     content="This service agreement outlines...",
#     metadata={"type": "Service Agreement", "created_by": "user-123", ...}
# )
```

### API Endpoints

#### Search Query

```bash
GET /api/search/query?q=acme&limit=20&resource_filter=customer

Response:
{
  "query": "acme",
  "results": [
    {
      "resource": "customer",
      "entity_id": "cust-001",
      "title": "Acme Corporation",
      "score": 0.95,
      "metadata": {"email": "contact@acme.com", ...}
    },
    ...
  ],
  "total": 3
}
```

#### List Resources

```bash
GET /api/search/resources

Response:
[
  {
    "resource_name": "customer",
    "description": "Customer records",
    "indexed": true,
    "entity_count": 3
  },
  {
    "resource_name": "company",
    "description": "Company/partner records",
    "indexed": true,
    "entity_count": 3
  },
  {
    "resource_name": "document",
    "description": "Business documents",
    "indexed": true,
    "entity_count": 2
  }
]
```

#### Index Entity

```bash
POST /api/search/index/customer/cust-123

Response:
{
  "resource": "customer",
  "entity_id": "cust-123",
  "status": "indexed",
  "message": "Successfully indexed cust-123"
}
```

#### Rebuild Index

```bash
POST /api/search/rebuild/customer

Response:
{
  "status": "rebuilding",
  "resource": "customer",
  "message": "Started rebuilding index for resource 'customer'"
}
```

---

## Files Implementation

### Models

#### FileStorageManager (`app/models/files.py`)

Central manager for file operations:

```python
from app.models.files import FileStorageManager

manager = FileStorageManager()

# Upload contract
contract = manager.upload_contract(
    filename="service_agreement.pdf",
    data=pdf_bytes,
    contract_type="Service Agreement",
    counterparty="Acme Corp",
    effective_date=datetime(2024, 1, 1),
    created_by="user-123",
)

# Create version
new_version = manager.create_version(
    file_id="file-123",
    new_filename="agreement_v2.pdf",
    data=updated_bytes,
    created_by="user-123",
    change_description="Updated payment terms",
)

# Download
filename, content = manager.download_file("file-123")

# List versions
versions = manager.list_versions("file-123")

# AI Operations (if enabled)
summary = manager.summarize_document("file-123")
answer = manager.ask_document("file-123", "What is the termination clause?")
```

#### Domain Models

**ContractDocument**
```python
from app.models.files import ContractDocument

contract = ContractDocument(
    file_id="file-123",
    contract_name="ABC-ACME Service Agreement",
    contract_type="Service Agreement",
    counterparty="Acme Corp",
    effective_date=datetime(2024, 1, 1),
    expiration_date=datetime(2025, 12, 31),
    status="signed",
    stored_by="user-123",
)
```

**PolicyDocument**
```python
from app.models.files import PolicyDocument

policy = PolicyDocument(
    file_id="file-456",
    policy_name="ABC Security Policy",
    policy_type="Security",
    version="2.1",
    effective_date=datetime(2024, 1, 1),
    status="active",
    stored_by="admin-001",
)
```

### API Endpoints

#### Upload File

```bash
POST /api/files/upload
Content-Type: multipart/form-data

file: <binary>
description: "Q4 2024 Service Agreement"
tags: "contract,legal,2024"

Response:
{
  "file_id": "file-001",
  "filename": "agreement.pdf",
  "size_bytes": 256000,
  "message": "Successfully uploaded agreement.pdf"
}
```

#### Download File

```bash
GET /api/files/download/file-123
GET /api/files/download/file-123?version=2  # Specific version

Response: [Binary file stream]
```

#### Create Version

```bash
POST /api/files/version/file-123
Content-Type: multipart/form-data

file: <updated binary>
change_description: "Updated payment terms per client request"

Response:
{
  "version_number": 2,
  "filename": "agreement_v2.pdf",
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": "user-123",
  "size_bytes": 260000,
  "is_current": true
}
```

#### List Versions

```bash
GET /api/files/versions/file-123

Response:
[
  {
    "version_number": 2,
    "filename": "agreement_v2.pdf",
    "created_at": "2024-01-15T10:30:00Z",
    "created_by": "user-123",
    "size_bytes": 260000,
    "is_current": true
  },
  {
    "version_number": 1,
    "filename": "agreement.pdf",
    "created_at": "2024-01-10T09:00:00Z",
    "created_by": "user-123",
    "size_bytes": 256000,
    "is_current": false
  }
]
```

#### Get Metadata

```bash
GET /api/files/file-123/metadata

Response:
{
  "id": "file-123",
  "filename": "agreement.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 256000,
  "version": 1,
  "created_at": "2024-01-10T09:00:00Z",
  "created_by": "user-123",
  "is_deleted": false
}
```

#### Delete File

```bash
DELETE /api/files/file-123

Response:
{
  "status": "deleted",
  "file_id": "file-123",
  "message": "File marked as deleted"
}
```

#### Restore File

```bash
POST /api/files/file-123/restore

Response:
{
  "status": "restored",
  "file_id": "file-123",
  "message": "File restored successfully"
}
```

#### AI Operations

**Summarize**
```bash
POST /api/files/file-123/ai/summarize

Response:
{
  "file_id": "file-123",
  "operation": "summarize",
  "result": "This is a summary of the document content...",
  "processing_time_ms": 1234.5
}
```

**Ask Question**
```bash
POST /api/files/file-123/ai/ask?question=What+is+the+termination+clause?

Response:
{
  "file_id": "file-123",
  "operation": "ask",
  "result": "Based on the document, the termination clause states...",
  "processing_time_ms": 2345.6
}
```

**Generate Content**
```bash
POST /api/files/file-123/ai/generate?prompt=Write+a+client-friendly+summary

Response:
{
  "file_id": "file-123",
  "operation": "generate",
  "result": "Generated content based on the document...",
  "processing_time_ms": 3456.7
}
```

---

## Integration Points

### Application Startup (`app/main.py`)

Both routers are registered during app initialization:

```python
from app.api import search, files

app.include_router(search.router)
app.include_router(files.router)
```

### Permission Seeding (`app/permissions/definitions.py`)

Search and file permissions are seeded alongside application permissions:

```python
SEARCH_ACCESS = "search.execute"
SEARCH_MANAGE = "search.manage"

FILES_UPLOAD = "file.upload"
FILES_VIEW = "file.view"
FILES_MANAGE = "file.manage"

PERMISSIONS: list[tuple[str, str]] = [
    (SEARCH_ACCESS, "Search across business resources"),
    (SEARCH_MANAGE, "Manage search indexes and configuration"),
    (FILES_UPLOAD, "Upload files to secure storage"),
    (FILES_VIEW, "Download and view files"),
    (FILES_MANAGE, "Manage files (versions, deletion, restoration)"),
]
```

### Database Schema

Both packages include SQL schema files:

- `perennia_search/schema.sql`: Search index tables
- `perennia_files/schema.sql`: File storage and versioning tables

Apply these during database initialization:

```bash
mysql -u app -p myapp < perennia_search/schema.sql
mysql -u app -p myapp < perennia_files/schema.sql
```

---

## Usage Examples

### Search for Customers

```python
# Search across all resources
curl "http://localhost:8000/api/search/query?q=acme&limit=10"

# Filter to customer resource
curl "http://localhost:8000/api/search/query?q=acme&resource_filter=customer"
```

### Upload and Version Documents

```python
# Upload initial contract
curl -X POST "http://localhost:8000/api/files/upload" \
  -F "file=@contract.pdf" \
  -F "description=ABC-ACME Service Agreement"

# Later, upload revised version
curl -X POST "http://localhost:8000/api/files/version/file-123" \
  -F "file=@contract_v2.pdf" \
  -F "change_description=Updated payment terms"

# Download latest version
curl "http://localhost:8000/api/files/download/file-123" \
  -o contract_latest.pdf

# Download specific version
curl "http://localhost:8000/api/files/download/file-123?version=1" \
  -o contract_v1.pdf
```

### AI-Assisted Document Analysis

```python
# Get AI summary of contract
curl -X POST "http://localhost:8000/api/files/file-123/ai/summarize"

# Ask specific question
curl -X POST "http://localhost:8000/api/files/file-123/ai/ask" \
  -G --data-urlencode "question=What is the termination clause?"

# Generate client-friendly summary
curl -X POST "http://localhost:8000/api/files/file-123/ai/generate" \
  -G --data-urlencode "prompt=Write a client-friendly summary"
```

---

## Permission Model

### Search Permissions

| Permission | Role | Purpose |
|-----------|------|---------|
| `search.execute` | Employee, Manager, Admin | Execute searches across resources |
| `search.manage` | Manager, Admin | Manage search indexes and providers |

### File Permissions

| Permission | Role | Purpose |
|-----------|------|---------|
| `file.upload` | Manager, Admin | Upload files to storage |
| `file.view` | Employee, Manager, Admin | Download and view files |
| `file.manage` | Manager, Admin | Create versions, delete, restore files |
| `file.ai` | Manager, Admin | Use AI processing on files |

### Role Matrix

| Role | Search | Files |
|------|--------|-------|
| Employee | execute | view |
| Manager | execute, manage | upload, view, manage |
| Administrator | execute, manage | upload, view, manage |

---

## Implementation Checklist

To integrate these components into a production application:

- [ ] Install dependencies: `pip install perennia-search perennia-files`
- [ ] Apply database schemas from both packages
- [ ] Configure PerenniaSearch with DatabaseConfig
- [ ] Configure PerenniaFiles with storage path and signing secret
- [ ] Create your domain-specific SearchProviders
- [ ] Connect FileStorageManager to PerenniaFiles instance
- [ ] Wire up actual database queries in model methods
- [ ] Enable AI processing if needed (see perennia-files documentation)
- [ ] Test authorization with perennia-access integration
- [ ] Update frontend to call new search and files endpoints

---

## See Also

- [perennia-search GitHub](https://github.com/BT-Rajan/perennia-search)
- [perennia-files GitHub](https://github.com/BT-Rajan/perennia-files)
- Main [README.md](./README.md) for application overview
