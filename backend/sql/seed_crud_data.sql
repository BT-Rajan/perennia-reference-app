-- ════════════════════════════════════════════════════════════════════════════
-- ABC Enterprises - CRUD Entities Seed Data
-- Development/testing seed data
-- ════════════════════════════════════════════════════════════════════════════

USE abc_enterprises;

-- ────────────────────────────────────────────────────────────────────────────
-- Clients
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO clients (name, email, phone, address, gstin, contact_person, payment_terms, credit_limit, status, notes) VALUES
('Acme Manufacturing Ltd', 'contact@acme.com', '+91-98765-43210', '123 Industrial Ave, Mumbai', '27AABTU1234H1Z0', 'Raj Kumar', 'Net 30', 500000.00, 'Active', 'Premium client - good payment history'),
('Global Trading Corp', 'sales@globaltrading.com', '+91-98765-43211', '456 Commerce St, Delhi', '07AABCT5678H2Z1', 'Priya Sharma', 'Net 45', 750000.00, 'Active', 'Key account - cement distributor'),
('Regional Supplies Inc', 'order@regional.com', '+91-98765-43212', '789 Supply Rd, Bangalore', '29AABCS9012H3Z2', 'Vikram Singh', 'Net 15', 300000.00, 'Active', 'Regular orders'),
('Coastal Exports Ltd', 'export@coastal.com', '+91-98765-43213', '321 Port Rd, Chennai', '33AABCE3456H4Z3', 'Sneha Desai', 'Net 60', 600000.00, 'Inactive', 'Seasonal orders'),
('Construction Hub', 'procurement@conhub.com', '+91-98765-43214', '654 Building Blvd, Pune', '27AABCH7890H5Z4', 'Arjun Reddy', 'Net 30', 400000.00, 'Active', 'Large volume orders');

-- ────────────────────────────────────────────────────────────────────────────
-- Raw Materials
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO raw_materials (name, unit, description, status) VALUES
('Limestone', 'kg', 'Crushed limestone - primary raw material', 'Active'),
('Gypsum', 'kg', 'Calcined gypsum for setting control', 'Active'),
('Silica Sand', 'kg', 'Fine silica sand - pozzolanic material', 'Active'),
('Iron Ore', 'kg', 'Iron oxide for color and strength', 'Active'),
('Fly Ash', 'kg', 'Waste product from thermal power plants', 'Active'),
('Quartz', 'kg', 'Crystalline quartz - mineral admixture', 'Active');

-- ────────────────────────────────────────────────────────────────────────────
-- Products
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO products (name, category, description, default_bag_size_kg, status) VALUES
('PPC Cement', 'Cement', 'Portland Pozzolana Cement - eco-friendly', 50, 'Active'),
('OPC Cement', 'Cement', 'Ordinary Portland Cement - standard grade', 50, 'Active'),
('White Cement', 'Specialty', 'Premium white cement for architectural use', 25, 'Active'),
('High Strength Cement', 'Specialty', 'HSC grade for high-rise applications', 50, 'Active'),
('Low Heat Cement', 'Specialty', 'LH grade for mass concrete', 50, 'Inactive');

-- ────────────────────────────────────────────────────────────────────────────
-- Formulas (Bill of Materials)
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO formulas (product_id, material_id, percentage, notes) VALUES
(1, 1, 65.5, 'Primary component'),
(1, 2, 5.0, 'Setting control'),
(1, 3, 20.0, 'Pozzolanic material'),
(1, 4, 3.5, 'Iron oxide'),
(1, 5, 6.0, 'Waste material utilization'),
(2, 1, 80.0, 'Clinker source'),
(2, 2, 5.0, 'Gypsum as retarder'),
(2, 4, 4.0, 'Iron oxide'),
(2, 6, 11.0, 'Silica source'),
(3, 1, 75.0, 'White limestone'),
(3, 2, 6.0, 'Setting control'),
(3, 3, 19.0, 'Fine silica');

-- ────────────────────────────────────────────────────────────────────────────
-- Suppliers
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO suppliers (name, contact_person, phone, email, address, gstin, category, rating, payment_terms, delivery_cost, status, notes) VALUES
('Stone Quarry Co', 'Rajeev Rao', '+91-97654-32109', 'supply@stonequarry.com', '100 Quarry Ln, Rajasthan', '08AABSQ1234H1Z0', 'Raw Materials', 5, 'Net 45', 5000.00, 'Active', 'Reliable limestone supplier'),
('Thermal Ash Ltd', 'Mohit Verma', '+91-97654-32108', 'ash@thermal.com', '200 Industrial Zone, Odisha', '21AABTH2345H2Z1', 'Waste Products', 4, 'Net 30', 3000.00, 'Active', 'Consistent fly ash quality'),
('Mineral Solutions', 'Anjali Singh', '+91-97654-32107', 'minerals@soln.com', '300 Chem Park, Gujarat', '24AABMS3456H3Z2', 'Chemicals', 4, 'Net 45', 4000.00, 'Active', 'Gypsum and additives'),
('Global Silica', 'David Chen', '+91-97654-32106', 'silica@global.com', '400 Trade Center, TN', '33AABGS4567H4Z3', 'Raw Materials', 3, 'Net 60', 6000.00, 'Inactive', 'Seasonal supply');

-- ────────────────────────────────────────────────────────────────────────────
-- Quotations
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO quotations (quotation_no, client_id, product_id, quantity_kg, bag_size_kg, bags, valid_until, status, priority, notes, approved_by, approved_at) VALUES
('QT-2024-0001', 1, 1, 5000, 50, 100, '2024-03-15', 'Approved', 'High', 'Bulk quotation - monthly supply', 'demo-administrator', '2024-02-10 09:30:00'),
('QT-2024-0002', 2, 2, 10000, 50, 200, '2024-03-20', 'Pending', 'Critical', 'Rush quotation - high strength', NULL, NULL),
('QT-2024-0003', 3, 1, 2500, 50, 50, '2024-03-25', 'Draft', 'Normal', 'Regular quotation', NULL, NULL),
('QT-2024-0004', 1, 3, 1000, 25, 40, '2024-04-05', 'Draft', 'Low', 'White cement - low volume', NULL, NULL),
('QT-2024-0005', 5, 2, 7500, 50, 150, '2024-03-28', 'Rejected', 'High', 'Construction project - budget declined', NULL, NULL);

-- ────────────────────────────────────────────────────────────────────────────
-- Orders (one per Approved quotation above - see quotation QT-2024-0001)
-- ────────────────────────────────────────────────────────────────────────────
INSERT IGNORE INTO orders (order_no, quotation_id, client_id, product_id, quantity_kg, bag_size_kg, bags, delivery_date, status, priority, notes) VALUES
('ORD-2024-0001', 1, 1, 1, 5000, 50, 100, '2024-03-01', 'Pending', 'High', 'Converted from quotation QT-2024-0001');
