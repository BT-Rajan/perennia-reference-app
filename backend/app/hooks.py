"""Business logic hooks for CRUD operations.

Hooks are optional objects with methods like:
  - before_create(data)
  - after_create(record)
  - before_update(existing, data)
  - after_update(record)
  - before_delete(existing)
  - after_delete(existing)
  - before_restore(existing)
  - after_restore(record)

These execute at predictable points in the CRUD lifecycle, allowing:
  - Validation and enrichment before persistence
  - Side effects after successful changes (logging, notifications, etc.)
  - Cascade operations (delete related records, update counts, etc.)

Each hook receives the relevant data and can raise exceptions to abort
the operation. perennia-crud never knows or cares what these hooks do —
business logic stays in the consuming module.
"""

import logging
from datetime import datetime

logger = logging.getLogger("perennia_crud_hooks")


# ═════════════════════════════════════════════════════════════════════════════
# Clients Hooks
# ═════════════════════════════════════════════════════════════════════════════

class ClientsHooks:
    """Business logic hooks for Client CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate client data before creation."""
        if not data.get("name"):
            raise ValueError("Client name is required")
        if data.get("credit_limit", 0) < 0:
            raise ValueError("Credit limit cannot be negative")

    @staticmethod
    def after_create(record: dict) -> None:
        """Log client creation."""
        logger.info(f"Client created: {record['id']} - {record['name']}")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate client updates."""
        if "credit_limit" in data and data["credit_limit"] < 0:
            raise ValueError("Credit limit cannot be negative")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log client update."""
        logger.info(f"Client updated: {record['id']} - {record['name']}")

    @staticmethod
    def before_delete(existing: dict) -> None:
        """Check if client can be deleted."""
        # Could check for related orders here
        logger.info(f"Client deletion initiated: {existing['id']} - {existing['name']}")

    @staticmethod
    def after_delete(existing: dict) -> None:
        """Log client deletion."""
        logger.info(f"Client soft-deleted: {existing['id']} - {existing['name']}")

    @staticmethod
    def before_restore(existing: dict) -> None:
        """Prepare for client restoration."""
        logger.info(f"Client restoration initiated: {existing['id']} - {existing['name']}")

    @staticmethod
    def after_restore(record: dict) -> None:
        """Log client restoration."""
        logger.info(f"Client restored: {record['id']} - {record['name']}")


# ═════════════════════════════════════════════════════════════════════════════
# Products Hooks
# ═════════════════════════════════════════════════════════════════════════════

class ProductsHooks:
    """Business logic hooks for Product CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate product data before creation."""
        if not data.get("name"):
            raise ValueError("Product name is required")
        if data.get("default_bag_size_kg", 0) <= 0:
            raise ValueError("Default bag size must be positive")

    @staticmethod
    def after_create(record: dict) -> None:
        """Log product creation."""
        logger.info(f"Product created: {record['id']} - {record['name']}")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate product updates."""
        if "default_bag_size_kg" in data and data["default_bag_size_kg"] <= 0:
            raise ValueError("Default bag size must be positive")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log product update."""
        logger.info(f"Product updated: {record['id']} - {record['name']}")

    @staticmethod
    def before_delete(existing: dict) -> None:
        """Check if product can be deleted."""
        logger.info(f"Product deletion initiated: {existing['id']} - {existing['name']}")

    @staticmethod
    def after_delete(existing: dict) -> None:
        """Log product deletion."""
        logger.info(f"Product soft-deleted: {existing['id']} - {existing['name']}")


# ═════════════════════════════════════════════════════════════════════════════
# Raw Materials Hooks
# ═════════════════════════════════════════════════════════════════════════════

class RawMaterialsHooks:
    """Business logic hooks for Raw Material CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate raw material data before creation."""
        if not data.get("name"):
            raise ValueError("Material name is required")
        if not data.get("unit"):
            data["unit"] = "kg"  # Default unit

    @staticmethod
    def after_create(record: dict) -> None:
        """Log raw material creation."""
        logger.info(f"Raw material created: {record['id']} - {record['name']}")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate raw material updates."""
        # Prevent critical field changes
        if "unit" in data and data["unit"] != existing.get("unit"):
            logger.warning(f"Unit change attempted for material {existing['id']}: {existing['unit']} -> {data['unit']}")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log raw material update."""
        logger.info(f"Raw material updated: {record['id']} - {record['name']}")

    @staticmethod
    def before_delete(existing: dict) -> None:
        """Check if material can be deleted (may have formulas)."""
        logger.info(f"Raw material deletion initiated: {existing['id']} - {existing['name']}")


# ═════════════════════════════════════════════════════════════════════════════
# Formulas Hooks
# ═════════════════════════════════════════════════════════════════════════════

class FormulasHooks:
    """Business logic hooks for Formula CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate formula data before creation."""
        if not data.get("product_id"):
            raise ValueError("Product ID is required")
        if not data.get("material_id"):
            raise ValueError("Material ID is required")
        
        percentage = data.get("percentage", 0)
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100")

    @staticmethod
    def after_create(record: dict) -> None:
        """Log formula creation."""
        logger.info(f"Formula created: product_id={record['product_id']}, material_id={record['material_id']}")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate formula updates."""
        # Prevent critical field changes
        if "product_id" in data and data["product_id"] != existing.get("product_id"):
            raise ValueError("Cannot change product for existing formula")
        if "material_id" in data and data["material_id"] != existing.get("material_id"):
            raise ValueError("Cannot change material for existing formula")
        
        if "percentage" in data:
            if data["percentage"] <= 0 or data["percentage"] > 100:
                raise ValueError("Percentage must be between 0 and 100")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log formula update."""
        logger.info(f"Formula updated: product_id={record['product_id']}, material_id={record['material_id']}")


# ═════════════════════════════════════════════════════════════════════════════
# Suppliers Hooks
# ═════════════════════════════════════════════════════════════════════════════

class SuppliersHooks:
    """Business logic hooks for Supplier CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate supplier data before creation."""
        if not data.get("name"):
            raise ValueError("Supplier name is required")
        if data.get("rating") is not None:
            if not (1 <= data["rating"] <= 5):
                raise ValueError("Rating must be between 1 and 5")

    @staticmethod
    def after_create(record: dict) -> None:
        """Log supplier creation."""
        logger.info(f"Supplier created: {record['id']} - {record['name']}")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate supplier updates."""
        if "rating" in data and data["rating"] is not None:
            if not (1 <= data["rating"] <= 5):
                raise ValueError("Rating must be between 1 and 5")
        if "delivery_cost" in data and data["delivery_cost"] < 0:
            raise ValueError("Delivery cost cannot be negative")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log supplier update."""
        logger.info(f"Supplier updated: {record['id']} - {record['name']}")

    @staticmethod
    def before_delete(existing: dict) -> None:
        """Check if supplier can be deleted."""
        logger.info(f"Supplier deletion initiated: {existing['id']} - {existing['name']}")


# ═════════════════════════════════════════════════════════════════════════════
# Orders Hooks
# ═════════════════════════════════════════════════════════════════════════════

class OrdersHooks:
    """Business logic hooks for Order CRUD operations."""

    @staticmethod
    def before_create(data: dict) -> None:
        """Validate order data before creation."""
        if not data.get("order_no"):
            raise ValueError("Order number is required")
        if not data.get("client_id"):
            raise ValueError("Client ID is required")
        if not data.get("product_id"):
            raise ValueError("Product ID is required")
        
        qty = data.get("quantity_kg", 0)
        if qty <= 0:
            raise ValueError("Quantity must be positive")

    @staticmethod
    def after_create(record: dict) -> None:
        """Log order creation."""
        logger.info(f"Order created: {record['id']} - {record['order_no']} (qty: {record['quantity_kg']}kg)")

    @staticmethod
    def before_update(existing: dict, data: dict) -> None:
        """Validate order updates."""
        # Prevent critical field changes for confirmed orders
        if existing.get("status") != "Pending":
            if "client_id" in data or "product_id" in data:
                raise ValueError(f"Cannot change client/product for {existing['status']} order")
        
        if "quantity_kg" in data and data["quantity_kg"] <= 0:
            raise ValueError("Quantity must be positive")

    @staticmethod
    def after_update(record: dict) -> None:
        """Log order update."""
        logger.info(f"Order updated: {record['id']} - {record['order_no']} (status: {record['status']})")

    @staticmethod
    def before_delete(existing: dict) -> None:
        """Validate order deletion."""
        if existing.get("status") in ("Shipped", "Closed"):
            raise ValueError(f"Cannot delete {existing['status']} order")

    @staticmethod
    def after_delete(existing: dict) -> None:
        """Log order deletion."""
        logger.info(f"Order soft-deleted: {existing['id']} - {existing['order_no']}")
