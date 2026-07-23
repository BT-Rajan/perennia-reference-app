"""CRUD API endpoints for business domain entities.

Each entity uses the perennia-crud CrudEngine instance defined in deps.py.
Routes follow REST conventions:
  - GET /api/{entity}         -> list with pagination
  - GET /api/{entity}/{id}    -> get one
  - POST /api/{entity}        -> create
  - PUT /api/{entity}/{id}    -> update
  - DELETE /api/{entity}/{id} -> soft delete
  - POST /api/{entity}/{id}/restore -> restore (soft delete only)
"""

from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from perennia_crud.query import ListQuery, PagedResult
from perennia_crud.exceptions import RecordNotFoundError
from perennia_access import AuthenticatedIdentity as Identity

from app.deps import (
    identity_required,
    require_permission,
    settings,
    access,
    crud_clients,
    crud_products,
    crud_raw_materials,
    crud_formulas,
    crud_suppliers,
    crud_quotations,
    crud_orders,
)
from app.permissions.definitions import QUOTATIONS_APPROVE
from app.hooks import quotation_approval_in_progress, order_creation_in_progress

router = APIRouter(prefix="/api", tags=["CRUD"])


# ═════════════════════════════════════════════════════════════════════════════
# Response Models
# ═════════════════════════════════════════════════════════════════════════════

class PaginationInfo(BaseModel):
    total: int
    page: int
    page_size: int


class ListResponseMeta(BaseModel):
    pagination: PaginationInfo


class ListResponse(BaseModel):
    data: List[dict]
    meta: ListResponseMeta


class CreateResponse(BaseModel):
    data: dict


class UpdateResponse(BaseModel):
    data: dict


class DeleteResponse(BaseModel):
    success: bool


# ═════════════════════════════════════════════════════════════════════════════
# Clients Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/clients", response_model=ListResponse)
def list_clients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all clients with optional filtering."""
    query = ListQuery(
        page=page,
        page_size=page_size,
        search=search,
        filters={"status": status} if status else {}
    )
    result = crud_clients.list(query, identity=identity)
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


@router.get("/clients/{client_id}")
def get_client(client_id: int, identity: Identity = Depends(identity_required)):
    """Get a single client by ID."""
    try:
        record = crud_clients.get(client_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")


@router.post("/clients", response_model=CreateResponse)
def create_client(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new client."""
    try:
        record = crud_clients.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/clients/{client_id}", response_model=UpdateResponse)
def update_client(
    client_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing client."""
    try:
        record = crud_clients.update(client_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/clients/{client_id}", response_model=DeleteResponse)
def delete_client(client_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) a client."""
    try:
        success = crud_clients.delete(client_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")


@router.post("/clients/{client_id}/restore")
def restore_client(client_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted client."""
    try:
        record = crud_clients.restore(client_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Client not found")


# ═════════════════════════════════════════════════════════════════════════════
# Products Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/products", response_model=ListResponse)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all products with optional filtering."""
    query = ListQuery(
        page=page,
        page_size=page_size,
        search=search,
        filters={"status": status} if status else {}
    )
    result = crud_products.list(query, identity=identity)
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


@router.get("/products/{product_id}")
def get_product(product_id: int, identity: Identity = Depends(identity_required)):
    """Get a single product by ID."""
    try:
        record = crud_products.get(product_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/products", response_model=CreateResponse)
def create_product(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new product."""
    try:
        record = crud_products.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/products/{product_id}", response_model=UpdateResponse)
def update_product(
    product_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing product."""
    try:
        record = crud_products.update(product_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/products/{product_id}", response_model=DeleteResponse)
def delete_product(product_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) a product."""
    try:
        success = crud_products.delete(product_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/products/{product_id}/restore")
def restore_product(product_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted product."""
    try:
        record = crud_products.restore(product_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")


# ═════════════════════════════════════════════════════════════════════════════
# Raw Materials Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/raw-materials", response_model=ListResponse)
def list_raw_materials(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all raw materials with optional filtering."""
    query = ListQuery(
        page=page,
        page_size=page_size,
        search=search,
        filters={"status": status} if status else {}
    )
    result = crud_raw_materials.list(query, identity=identity)
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


@router.get("/raw-materials/{material_id}")
def get_raw_material(
    material_id: int,
    identity: Identity = Depends(identity_required)
):
    """Get a single raw material by ID."""
    try:
        record = crud_raw_materials.get(material_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Raw material not found")


@router.post("/raw-materials", response_model=CreateResponse)
def create_raw_material(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new raw material."""
    try:
        record = crud_raw_materials.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/raw-materials/{material_id}", response_model=UpdateResponse)
def update_raw_material(
    material_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing raw material."""
    try:
        record = crud_raw_materials.update(material_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Raw material not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/raw-materials/{material_id}", response_model=DeleteResponse)
def delete_raw_material(
    material_id: int,
    identity: Identity = Depends(identity_required)
):
    """Delete (soft delete) a raw material."""
    try:
        success = crud_raw_materials.delete(material_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Raw material not found")


@router.post("/raw-materials/{material_id}/restore")
def restore_raw_material(
    material_id: int,
    identity: Identity = Depends(identity_required)
):
    """Restore a soft-deleted raw material."""
    try:
        record = crud_raw_materials.restore(material_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Raw material not found")


# ═════════════════════════════════════════════════════════════════════════════
# Formulas Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/formulas", response_model=ListResponse)
def list_formulas(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_id: Optional[int] = None,
    identity: Identity = Depends(identity_required),
):
    """List all formulas with optional filtering by product."""
    query = ListQuery(
        page=page,
        page_size=page_size,
        filters={"product_id": product_id} if product_id else {}
    )
    result = crud_formulas.list(query, identity=identity)
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


@router.get("/formulas/{formula_id}")
def get_formula(formula_id: int, identity: Identity = Depends(identity_required)):
    """Get a single formula by ID."""
    try:
        record = crud_formulas.get(formula_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Formula not found")


@router.post("/formulas", response_model=CreateResponse)
def create_formula(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new formula."""
    try:
        record = crud_formulas.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/formulas/{formula_id}", response_model=UpdateResponse)
def update_formula(
    formula_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing formula."""
    try:
        record = crud_formulas.update(formula_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Formula not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/formulas/{formula_id}", response_model=DeleteResponse)
def delete_formula(formula_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) a formula."""
    try:
        success = crud_formulas.delete(formula_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Formula not found")


@router.post("/formulas/{formula_id}/restore")
def restore_formula(formula_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted formula."""
    try:
        record = crud_formulas.restore(formula_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Formula not found")


# ═════════════════════════════════════════════════════════════════════════════
# Suppliers Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/suppliers", response_model=ListResponse)
def list_suppliers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all suppliers with optional filtering."""
    query = ListQuery(
        page=page,
        page_size=page_size,
        search=search,
        filters={"status": status} if status else {}
    )
    result = crud_suppliers.list(query, identity=identity)
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


@router.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int, identity: Identity = Depends(identity_required)):
    """Get a single supplier by ID."""
    try:
        record = crud_suppliers.get(supplier_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Supplier not found")


@router.post("/suppliers", response_model=CreateResponse)
def create_supplier(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new supplier."""
    try:
        record = crud_suppliers.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/suppliers/{supplier_id}", response_model=UpdateResponse)
def update_supplier(
    supplier_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing supplier."""
    try:
        record = crud_suppliers.update(supplier_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Supplier not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/suppliers/{supplier_id}", response_model=DeleteResponse)
def delete_supplier(supplier_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) a supplier."""
    try:
        success = crud_suppliers.delete(supplier_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Supplier not found")


@router.post("/suppliers/{supplier_id}/restore")
def restore_supplier(supplier_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted supplier."""
    try:
        record = crud_suppliers.restore(supplier_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Supplier not found")


# ═════════════════════════════════════════════════════════════════════════════
# Quotations Endpoints
#
# Creation is restricted to QUOTATION_CREATOR_ROLE (.env) via the
# quotations.create permission, enforced inside CrudEngine.create().
# Approval has its own dedicated endpoint and its own permission,
# quotations.approve, restricted to QUOTATION_APPROVER_ROLE (.env) - it is
# NOT available through the generic update endpoint below (see
# QuotationsHooks.before_update in app/hooks.py).
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/quotations", response_model=ListResponse)
def list_quotations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all quotations with optional filtering."""
    filters = {}
    if client_id:
        filters["client_id"] = client_id
    if status:
        filters["status"] = status

    query = ListQuery(page=page, page_size=page_size, filters=filters)
    result = crud_quotations.list(query, identity=identity)
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


@router.get("/quotations/{quotation_id}")
def get_quotation(quotation_id: int, identity: Identity = Depends(identity_required)):
    """Get a single quotation by ID."""
    try:
        record = crud_quotations.get(quotation_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")


@router.post("/quotations", response_model=CreateResponse)
def create_quotation(data: dict, identity: Identity = Depends(identity_required)):
    """Create a new quotation.

    Restricted to the role named by QUOTATION_CREATOR_ROLE in .env - enforced
    via the quotations.create permission, which is granted only to that role
    (see app/permissions/definitions.py:seed).
    """
    try:
        record = crud_quotations.create(data, identity=identity)
        return CreateResponse(data=record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/quotations/{quotation_id}", response_model=UpdateResponse)
def update_quotation(
    quotation_id: int,
    data: dict,
    identity: Identity = Depends(identity_required)
):
    """Update an existing quotation.

    Cannot be used to approve a quotation - status can never be set to
    "Approved" through this endpoint (see QuotationsHooks.before_update).
    Use POST /api/quotations/{quotation_id}/approve instead.
    """
    try:
        record = crud_quotations.update(quotation_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/quotations/{quotation_id}", response_model=DeleteResponse)
def delete_quotation(quotation_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) a quotation."""
    try:
        success = crud_quotations.delete(quotation_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")


@router.post("/quotations/{quotation_id}/restore")
def restore_quotation(quotation_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted quotation."""
    try:
        record = crud_quotations.restore(quotation_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")


@router.post("/quotations/{quotation_id}/approve", response_model=UpdateResponse)
def approve_quotation(
    quotation_id: int,
    identity: Identity = Depends(require_permission(QUOTATIONS_APPROVE)),
):
    """Approve a quotation.

    Restricted to the role named by QUOTATION_APPROVER_ROLE in .env -
    enforced via the quotations.approve permission, which is granted only to
    that role (see app/permissions/definitions.py:seed). This is the only
    endpoint that may move a quotation's status to "Approved".
    """
    try:
        existing = crud_quotations.get(quotation_id, identity=identity)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if existing.get("status") == "Approved":
        raise HTTPException(status_code=400, detail="Quotation is already approved")

    token = quotation_approval_in_progress.set(True)
    try:
        record = crud_quotations.update(
            quotation_id,
            {
                "status": "Approved",
                "approved_by": identity.subject_id,
                "approved_at": datetime.now(timezone.utc).isoformat(),
            },
            identity=identity,
        )
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Quotation not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        quotation_approval_in_progress.reset(token)

    # The only place an order is ever created. order_creation_in_progress
    # gates OrdersHooks.before_create - no other code path can pass it.
    order_token = order_creation_in_progress.set(True)
    try:
        crud_orders.create(
            {
                "order_no": f"ORD-{record['quotation_no']}",
                "quotation_id": record["id"],
                "client_id": record["client_id"],
                "product_id": record["product_id"],
                "quantity_kg": record["quantity_kg"],
                "bag_size_kg": record["bag_size_kg"],
                "bags": record["bags"],
            },
            identity=identity,
        )
    finally:
        order_creation_in_progress.reset(order_token)

    return UpdateResponse(data=record)


# ═════════════════════════════════════════════════════════════════════════════
# Orders Endpoints
#
# There is deliberately no POST /api/orders route. Orders are only ever
# created inside approve_quotation() above - see order_creation_in_progress
# in app/hooks.py, which OrdersHooks.before_create enforces regardless of
# how create() is invoked.
# ═════════════════════════════════════════════════════════════════════════════

@router.get("/orders", response_model=ListResponse)
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    identity: Identity = Depends(identity_required),
):
    """List all orders with optional filtering."""
    filters = {}
    if client_id:
        filters["client_id"] = client_id
    if status:
        filters["status"] = status

    query = ListQuery(page=page, page_size=page_size, filters=filters)
    result = crud_orders.list(query, identity=identity)
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


@router.get("/orders/{order_id}")
def get_order(order_id: int, identity: Identity = Depends(identity_required)):
    """Get a single order by ID."""
    try:
        record = crud_orders.get(order_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@router.put("/orders/{order_id}", response_model=UpdateResponse)
def update_order(order_id: int, data: dict, identity: Identity = Depends(identity_required)):
    """Update an existing order (e.g. fulfillment status)."""
    try:
        record = crud_orders.update(order_id, data, identity=identity)
        return UpdateResponse(data=record)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/orders/{order_id}", response_model=DeleteResponse)
def delete_order(order_id: int, identity: Identity = Depends(identity_required)):
    """Delete (soft delete) an order."""
    try:
        success = crud_orders.delete(order_id, identity=identity)
        return DeleteResponse(success=success)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")


@router.post("/orders/{order_id}/restore")
def restore_order(order_id: int, identity: Identity = Depends(identity_required)):
    """Restore a soft-deleted order."""
    try:
        record = crud_orders.restore(order_id, identity=identity)
        return {"data": record}
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
