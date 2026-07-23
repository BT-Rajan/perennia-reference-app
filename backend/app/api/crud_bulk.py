"""Bulk operations for CRUD entities.

Provides endpoints for:
  - Bulk create (multiple records at once)
  - Bulk update (multiple records with different data)
  - Bulk delete (multiple records at once)
  - Bulk restore (soft-deleted records)
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException

from perennia_access import AuthenticatedIdentity as Identity

from app.deps import (
    identity_required,
    crud_clients,
    crud_products,
    crud_raw_materials,
    crud_formulas,
    crud_suppliers,
    crud_quotations,
)

router = APIRouter(prefix="/api/bulk", tags=["Bulk Operations"])


# ═════════════════════════════════════════════════════════════════════════════
# Clients Bulk Operations
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/clients/create")
def bulk_create_clients(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple clients."""
    try:
        created = crud_clients.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clients/update")
def bulk_update_clients(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple clients.
    
    Each item in updates should have:
    {
        "id": <client_id>,
        "data": {<fields to update>}
    }
    """
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_clients.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clients/delete")
def bulk_delete_clients(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple clients."""
    try:
        count = crud_clients.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/clients/restore")
def bulk_restore_clients(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted clients."""
    try:
        restored = crud_clients.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═════════════════════════════════════════════════════════════════════════════
# Products Bulk Operations
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/products/create")
def bulk_create_products(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple products."""
    try:
        created = crud_products.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/update")
def bulk_update_products(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple products."""
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_products.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/delete")
def bulk_delete_products(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple products."""
    try:
        count = crud_products.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/restore")
def bulk_restore_products(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted products."""
    try:
        restored = crud_products.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═════════════════════════════════════════════════════════════════════════════
# Raw Materials Bulk Operations
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/raw-materials/create")
def bulk_create_raw_materials(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple raw materials."""
    try:
        created = crud_raw_materials.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/raw-materials/update")
def bulk_update_raw_materials(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple raw materials."""
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_raw_materials.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/raw-materials/delete")
def bulk_delete_raw_materials(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple raw materials."""
    try:
        count = crud_raw_materials.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/raw-materials/restore")
def bulk_restore_raw_materials(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted raw materials."""
    try:
        restored = crud_raw_materials.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═════════════════════════════════════════════════════════════════════════════
# Formulas Bulk Operations
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/formulas/create")
def bulk_create_formulas(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple formulas."""
    try:
        created = crud_formulas.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formulas/update")
def bulk_update_formulas(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple formulas."""
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_formulas.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formulas/delete")
def bulk_delete_formulas(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple formulas."""
    try:
        count = crud_formulas.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formulas/restore")
def bulk_restore_formulas(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted formulas."""
    try:
        restored = crud_formulas.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═════════════════════════════════════════════════════════════════════════════
# Suppliers Bulk Operations
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/suppliers/create")
def bulk_create_suppliers(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple suppliers."""
    try:
        created = crud_suppliers.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/suppliers/update")
def bulk_update_suppliers(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple suppliers."""
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_suppliers.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/suppliers/delete")
def bulk_delete_suppliers(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple suppliers."""
    try:
        count = crud_suppliers.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/suppliers/restore")
def bulk_restore_suppliers(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted suppliers."""
    try:
        restored = crud_suppliers.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═════════════════════════════════════════════════════════════════════════════
# Quotations Bulk Operations
#
# bulk_create still goes through CrudEngine.create() per record, so
# quotations.create (QUOTATION_CREATOR_ROLE) is enforced the same as the
# single-record endpoint. There is no bulk approve - approval always goes
# through POST /api/quotations/{id}/approve one at a time.
# ═════════════════════════════════════════════════════════════════════════════

@router.post("/quotations/create")
def bulk_create_quotations(
    records: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk create multiple quotations."""
    try:
        created = crud_quotations.bulk_create(records, identity=identity)
        return {"data": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quotations/update")
def bulk_update_quotations(
    updates: List[dict],
    identity: Identity = Depends(identity_required),
):
    """Bulk update multiple quotations. Cannot be used to approve quotations."""
    try:
        update_tuples = [(item["id"], item["data"]) for item in updates]
        updated = crud_quotations.bulk_update(update_tuples, identity=identity)
        return {"data": updated, "count": len(updated)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quotations/delete")
def bulk_delete_quotations(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk delete (soft delete) multiple quotations."""
    try:
        count = crud_quotations.bulk_delete(ids, identity=identity)
        return {"deleted": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quotations/restore")
def bulk_restore_quotations(
    ids: List[int],
    identity: Identity = Depends(identity_required),
):
    """Bulk restore multiple soft-deleted quotations."""
    try:
        restored = crud_quotations.bulk_restore(ids, identity=identity)
        return {"data": restored, "count": len(restored)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
