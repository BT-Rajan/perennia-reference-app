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

# Orders entity
orders = EntitySchema(
    table="orders",
    fields=[
        "order_no", "client_id", "product_id", "quantity_kg", "bag_size_kg",
        "bags", "delivery_date", "status", "priority", "notes", "quotation_no"
    ],
    primary_key="id",
    soft_delete=True,
    soft_delete_column="deleted_at",
    permission_prefix="orders"
)
