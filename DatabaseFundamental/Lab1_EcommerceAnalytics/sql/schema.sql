-- =============================================================================
-- E-Commerce Database Schema (3NF - Third Normal Form)
-- PostgreSQL DDL Statements
-- =============================================================================

-- Drop existing tables if they exist (for reset)
-- DROP TABLE IF EXISTS order_status_history CASCADE;
-- DROP TABLE IF EXISTS order_items CASCADE;
-- DROP TABLE IF EXISTS orders CASCADE;
-- DROP TABLE IF EXISTS products CASCADE;
-- DROP TABLE IF EXISTS categories CASCADE;
-- DROP TABLE IF EXISTS customers CASCADE;

-- =============================================================================
-- CATEGORIES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_name_not_empty CHECK (name != '')
);

COMMENT ON TABLE categories IS 'Product categories in the e-commerce catalog';
COMMENT ON COLUMN categories.name IS 'Unique category name';

-- =============================================================================
-- CUSTOMERS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_first_name_not_empty CHECK (first_name != ''),
    CONSTRAINT check_last_name_not_empty CHECK (last_name != ''),
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(city);

COMMENT ON TABLE customers IS 'Customer information with contact details';
COMMENT ON COLUMN customers.email IS 'Unique email address for customer identification';

-- =============================================================================
-- PRODUCTS TABLE with JSONB for flexible metadata
-- =============================================================================
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    CONSTRAINT check_price_positive CHECK (price >= 0),
    CONSTRAINT check_stock_non_negative CHECK (stock_quantity >= 0),
    CONSTRAINT check_name_not_empty CHECK (name != '')
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
-- GIN index for efficient JSONB queries
CREATE INDEX IF NOT EXISTS idx_products_metadata_gin ON products USING GIN(metadata);

COMMENT ON TABLE products IS 'Product catalog with flexible JSONB metadata (sizes, colors, etc)';
COMMENT ON COLUMN products.metadata IS 'JSONB field for flexible attributes like sizes, colors, brand, dimensions';
COMMENT ON COLUMN products.stock_quantity IS 'Current inventory count';

-- =============================================================================
-- ORDERS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT check_total_non_negative CHECK (total_amount >= 0)
);

-- B-tree index on customer_id for fast customer order lookups
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
-- Composite index for filtering by customer and date
CREATE INDEX IF NOT EXISTS idx_orders_customer_created ON orders(customer_id, created_at DESC);
-- Index on status for reporting
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

COMMENT ON TABLE orders IS 'Customer orders with transactional support';
COMMENT ON COLUMN orders.status IS 'Order status: pending, confirmed, shipped, delivered, or cancelled';
COMMENT ON COLUMN orders.total_amount IS 'Total order value calculated from order items';

-- =============================================================================
-- ORDER_ITEMS TABLE (Normalization: separate line items from orders)
-- =============================================================================
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    subtotal NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    CONSTRAINT check_quantity_positive CHECK (quantity > 0),
    CONSTRAINT check_unit_price_non_negative CHECK (unit_price >= 0),
    CONSTRAINT check_subtotal_non_negative CHECK (subtotal >= 0)
);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

COMMENT ON TABLE order_items IS 'Line items in orders (normalized separation from orders)';
COMMENT ON COLUMN order_items.subtotal IS 'Calculated as quantity * unit_price at time of purchase';

-- =============================================================================
-- ORDER_STATUS_HISTORY TABLE (Audit trail for order status changes)
-- =============================================================================
CREATE TABLE IF NOT EXISTS order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,

    CONSTRAINT fk_order_history FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_order_status_history_order ON order_status_history(order_id);
CREATE INDEX IF NOT EXISTS idx_order_status_history_changed ON order_status_history(changed_at DESC);

COMMENT ON TABLE order_status_history IS 'Audit trail tracking all status changes for an order';

-- =============================================================================
-- NORMALIZATION NOTES
-- =============================================================================
/*
FIRST NORMAL FORM (1NF):
- All attributes contain only atomic (indivisible) values
- No repeating groups of columns
- Example: order_items is separated from orders to avoid repeating columns

SECOND NORMAL FORM (2NF):
- Meets 1NF requirements
- All non-key attributes depend on the entire primary key
- No partial dependencies
- Example: subtotal in order_items depends on both order_id and product_id

THIRD NORMAL FORM (3NF):
- Meets 2NF requirements
- No transitive dependencies
- Non-key attributes depend only on the primary key
- Example: categories are separate because product properties shouldn't define product

JSONB FLEXIBILITY:
- Products.metadata allows flexible attributes without schema changes
- Avoids over-normalization for attributes that vary widely
- Example: Electronics need "processor" and "RAM" while Clothing needs "sizes" and "colors"
*/

-- =============================================================================
-- VIEWS FOR ANALYTICS
-- =============================================================================

CREATE OR REPLACE VIEW v_customer_order_summary AS
SELECT
    c.id as customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.email,
    COUNT(DISTINCT o.id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
GROUP BY c.id, c.first_name, c.last_name, c.email;

COMMENT ON VIEW v_customer_order_summary IS 'Customer order statistics for analytics';

CREATE OR REPLACE VIEW v_product_sales AS
SELECT
    p.id,
    p.name,
    c.name as category,
    COUNT(oi.id) as total_items_sold,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue,
    AVG(oi.unit_price) as avg_price
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name, c.name;

COMMENT ON VIEW v_product_sales IS 'Product sales analytics';

