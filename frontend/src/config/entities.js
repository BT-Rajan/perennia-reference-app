/**
 * One config object per CRUD entity. ResourceCrudPage.vue renders a full
 * list/create/edit/delete/restore page from nothing but this - entity
 * pages themselves are a couple of lines (see pages/ClientsPage.vue etc).
 *
 * fields   -> the create/edit form
 * columns  -> the list table
 * field.type: text (default) | number | date | textarea | select | reference
 * reference fields render as a <select> populated from another entity's
 * list endpoint (see field.reference / field.referenceLabelKey).
 */
export const entityConfigs = {
  clients: {
    label: "Clients",
    icon: "\u{1F465}",
    apiPath: "/api/clients",
    permissionPrefix: "clients",
    columns: [
      { key: "name", label: "Name" },
      { key: "contact_person", label: "Contact" },
      { key: "phone", label: "Phone" },
      { key: "payment_terms", label: "Terms" },
      { key: "status", label: "Status" },
    ],
    fields: [
      { key: "name", label: "Name", required: true },
      { key: "email", label: "Email" },
      { key: "phone", label: "Phone" },
      { key: "address", label: "Address", type: "textarea" },
      { key: "gstin", label: "GSTIN" },
      { key: "contact_person", label: "Contact Person" },
      { key: "payment_terms", label: "Payment Terms" },
      { key: "credit_limit", label: "Credit Limit", type: "number", step: "0.01", default: 0 },
      { key: "status", label: "Status", type: "select", options: ["Active", "Inactive"], default: "Active" },
      { key: "notes", label: "Notes", type: "textarea" },
    ],
  },

  products: {
    label: "Products",
    icon: "\u{1F4E6}",
    apiPath: "/api/products",
    permissionPrefix: "products",
    columns: [
      { key: "name", label: "Name" },
      { key: "category", label: "Category" },
      { key: "default_bag_size_kg", label: "Bag Size (kg)" },
      { key: "status", label: "Status" },
    ],
    fields: [
      { key: "name", label: "Name", required: true },
      { key: "category", label: "Category" },
      { key: "description", label: "Description", type: "textarea" },
      { key: "default_bag_size_kg", label: "Default Bag Size (kg)", type: "number", step: "0.001", default: 50 },
      { key: "status", label: "Status", type: "select", options: ["Active", "Inactive"], default: "Active" },
    ],
  },

  raw_materials: {
    label: "Raw Materials",
    icon: "\u{1FAA8}",
    apiPath: "/api/raw_materials",
    permissionPrefix: "raw_materials",
    columns: [
      { key: "name", label: "Name" },
      { key: "unit", label: "Unit" },
      { key: "supplier_id", label: "Supplier", type: "reference", reference: "suppliers" },
      { key: "status", label: "Status" },
    ],
    fields: [
      { key: "name", label: "Name", required: true },
      { key: "unit", label: "Unit", default: "kg" },
      { key: "description", label: "Description", type: "textarea" },
      { key: "supplier_id", label: "Supplier", type: "reference", reference: "suppliers" },
      { key: "status", label: "Status", type: "select", options: ["Active", "Inactive"], default: "Active" },
    ],
  },

  suppliers: {
    label: "Suppliers",
    icon: "\u{1F69A}",
    apiPath: "/api/suppliers",
    permissionPrefix: "suppliers",
    columns: [
      { key: "name", label: "Name" },
      { key: "contact_person", label: "Contact" },
      { key: "category", label: "Category" },
      { key: "rating", label: "Rating" },
      { key: "status", label: "Status" },
    ],
    fields: [
      { key: "name", label: "Name", required: true },
      { key: "contact_person", label: "Contact Person" },
      { key: "phone", label: "Phone" },
      { key: "email", label: "Email" },
      { key: "address", label: "Address", type: "textarea" },
      { key: "gstin", label: "GSTIN" },
      { key: "category", label: "Category" },
      { key: "rating", label: "Rating (1-5)", type: "number", step: "1" },
      { key: "payment_terms", label: "Payment Terms" },
      { key: "delivery_cost", label: "Delivery Cost", type: "number", step: "0.01", default: 0 },
      { key: "status", label: "Status", type: "select", options: ["Active", "Inactive"], default: "Active" },
      { key: "notes", label: "Notes", type: "textarea" },
    ],
  },

  quotations: {
    label: "Quotations",
    icon: "\u{1F4DD}",
    apiPath: "/api/quotations",
    permissionPrefix: "quotations",
    columns: [
      { key: "quotation_no", label: "Quotation No" },
      { key: "client_id", label: "Client", type: "reference", reference: "clients" },
      { key: "product_id", label: "Product", type: "reference", reference: "products" },
      { key: "quantity_kg", label: "Qty (kg)" },
      { key: "priority", label: "Priority" },
      { key: "status", label: "Status" },
    ],
    fields: [
      { key: "quotation_no", label: "Quotation No", required: true },
      { key: "client_id", label: "Client", type: "reference", reference: "clients", required: true },
      { key: "product_id", label: "Product", type: "reference", reference: "products", required: true },
      { key: "quantity_kg", label: "Quantity (kg)", type: "number", step: "0.001", required: true },
      { key: "bag_size_kg", label: "Bag Size (kg)", type: "number", step: "0.001", default: 50 },
      { key: "bags", label: "Bags", type: "number", step: "1", default: 0 },
      { key: "valid_until", label: "Valid Until", type: "date" },
      { key: "priority", label: "Priority", type: "select", options: ["Critical", "High", "Normal", "Low"], default: "Normal" },
      // "Approved" is deliberately not offered here - only
      // POST /api/quotations/{id}/approve may set that status.
      { key: "status", label: "Status", type: "select", options: ["Draft", "Pending", "Rejected", "Expired"], default: "Draft" },
      { key: "notes", label: "Notes", type: "textarea" },
    ],
  },
};
