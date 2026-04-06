-- =============================================================================
-- Index Creation for Query Optimization
-- =============================================================================

-- B-tree indexes for fast lookups on customer_id
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);

-- Composite index for customer and date filtering
CREATE INDEX IF NOT EXISTS idx_orders_customer_created ON orders(customer_id, created_at DESC);

-- Index on order status for reporting queries
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- GIN index for JSONB metadata queries (efficient for flexible attributes)
CREATE INDEX IF NOT EXISTS idx_products_metadata_gin ON products USING GIN(metadata);

-- B-tree indexes on foreign keys
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

-- Category and name lookups
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);

-- Customer email lookup
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(city);

-- Order status history tracking
CREATE INDEX IF NOT EXISTS idx_order_status_history_order ON order_status_history(order_id);
CREATE INDEX IF NOT EXISTS idx_order_status_history_changed ON order_status_history(changed_at DESC);

-- =============================================================================
-- ANALYZE INDEXES EFFECTIVENESS
-- =============================================================================

-- After data is populated, run:
-- ANALYZE products;
-- ANALYZE orders;
-- ANALYZE customers;
-- ANALYZE order_items;

-- Then use EXPLAIN ANALYZE to verify index usage:
-- EXPLAIN ANALYZE
-- SELECT * FROM orders WHERE customer_id = 1 ORDER BY created_at DESC;

