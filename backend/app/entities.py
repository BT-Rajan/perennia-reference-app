"""Entity schema definitions for perennia-crud."""

from perennia_crud.schema import EntitySchema

# Clients entity
clients = EntitySchema(
    table="clients",
    fields=[
        "name", "email", "phone", "address", "gstin", "contact_person",
        "payment_terms", "credit_limit", "status", "notes"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="clients"
)

# Products entity
products = EntitySchema(
    table="products",
    fields=[
        "name", "category", "description", "default_bag_size_kg", "status"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="products"
)

# Raw Materials entity
raw_materials = EntitySchema(
    table="raw_materials",
    fields=[
        "name", "unit", "description", "supplier_id", "status"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="raw_materials"
)

# Formulas entity
formulas = EntitySchema(
    table="formulas",
    fields=[
        "product_id", "material_id", "percentage", "notes"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="formulas"
)

# Suppliers entity
suppliers = EntitySchema(
    table="suppliers",
    fields=[
        "name", "contact_person", "phone", "email", "address", "gstin",
        "category", "rating", "payment_terms", "delivery_cost", "status", "notes"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="suppliers"
)

# Quotations entity
#
# Creation and approval are additionally gated by role - see
# QUOTATION_CREATOR_ROLE / QUOTATION_APPROVER_ROLE in .env, enforced via the
# quotations.create / quotations.approve permissions in
# app/permissions/definitions.py. approved_by / approved_at are listed here
# so the CRUD engine can write them, but app/hooks.py:QuotationsHooks blocks
# the generic update path from ever setting status to "Approved" - only the
# dedicated POST /api/quotations/{id}/approve endpoint may do that.
quotations = EntitySchema(
    table="quotations",
    fields=[
        "quotation_no", "client_id", "product_id", "quantity_kg", "bag_size_kg",
        "bags", "valid_until", "status", "priority", "notes", "approved_by", "approved_at"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="quotations"
)
