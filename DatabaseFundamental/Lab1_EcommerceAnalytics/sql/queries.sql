-- =============================================================================
-- Complex Analytical Queries
-- =============================================================================

-- QUERY 1: Top Selling Products with Window Functions
-- Ranks products by sales volume within each category
-- =============================================================================
WITH product_sales AS (
    SELECT
        p.id,
        p.name,
        p.category_id,
        c.name as category_name,
        SUM(oi.quantity) as total_sales,
        SUM(oi.subtotal) as total_revenue,
        RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as category_rank,
        ROW_NUMBER() OVER (ORDER BY SUM(oi.quantity) DESC) as overall_rank
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.id
    WHERE o.status != 'cancelled' OR o.id IS NULL
    GROUP BY p.id, p.name, p.category_id, c.name
)
SELECT
    id,
    name,
    category_name,
    total_sales,
    total_revenue,
    category_rank,
    overall_rank
FROM product_sales
WHERE total_sales > 0
ORDER BY overall_rank LIMIT 10;

-- QUERY 2: Customer Lifetime Value with CTEs
-- Uses Common Table Expression to calculate customer metrics
-- =============================================================================
WITH customer_orders AS (
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        COUNT(o.id) as total_orders,
        SUM(o.total_amount) as lifetime_value,
        AVG(o.total_amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        MIN(o.order_date) as first_order_date,
        DATEDIFF(DAY, MIN(o.order_date), MAX(o.order_date)) as customer_tenure_days
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
    GROUP BY c.id, c.first_name, c.last_name
)
SELECT
    id as customer_id,
    CONCAT(first_name, ' ', last_name) as customer_name,
    total_orders,
    COALESCE(lifetime_value, 0) as lifetime_value,
    COALESCE(avg_order_value, 0) as avg_order_value,
    last_order_date,
    first_order_date,
    customer_tenure_days
FROM customer_orders
ORDER BY lifetime_value DESC NULLS LAST;

-- QUERY 3: Product Ranking by Category with Multiple Window Functions
-- Demonstrates RANK, DENSE_RANK, and ROW_NUMBER
-- =============================================================================
SELECT
    p.id,
    p.name,
    c.name as category_name,
    COALESCE(SUM(oi.quantity), 0) as total_sales,
    COALESCE(SUM(oi.subtotal), 0) as total_revenue,
    RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as rank_in_category,
    DENSE_RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as dense_rank_in_category,
    ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as row_num_in_category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
GROUP BY p.id, p.name, c.name, p.category_id
ORDER BY c.name, rank_in_category;

-- QUERY 4: Customer Segmentation with CASE and Window Functions
-- Segments customers based on order frequency
-- =============================================================================
WITH customer_stats AS (
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        COUNT(o.id) as order_count,
        SUM(o.total_amount) as total_spent,
        CASE
            WHEN COUNT(o.id) = 0 THEN 'No Orders'
            WHEN COUNT(o.id) = 1 THEN 'Single Order'
            WHEN COUNT(o.id) BETWEEN 2 AND 5 THEN 'Regular'
            ELSE 'Frequent'
        END as customer_segment,
        ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) as wealth_rank
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
    GROUP BY c.id, c.first_name, c.last_name
)
SELECT
    id as customer_id,
    CONCAT(first_name, ' ', last_name) as customer_name,
    order_count,
    COALESCE(total_spent, 0) as total_spent,
    customer_segment,
    wealth_rank
FROM customer_stats
ORDER BY wealth_rank;

-- QUERY 5: Find Products by Metadata Attributes (GIN Index)
-- Uses -> and ->> operators to query JSONB
-- Should use idx_products_metadata_gin index
-- =============================================================================
SELECT
    id,
    name,
    price,
    stock_quantity,
    metadata->>'brand' as brand,
    metadata->>'color' as color
FROM products
WHERE metadata ->> 'brand' = 'TechBrand'
ORDER BY name;

-- QUERY 6: Sales Summary by Date Range
-- Complex aggregation with window functions
-- =============================================================================
WITH daily_sales AS (
    SELECT
        DATE(o.order_date) as order_date,
        COUNT(o.id) as order_count,
        SUM(o.total_amount) as daily_revenue,
        AVG(o.total_amount) as avg_order_value,
        COUNT(DISTINCT o.customer_id) as unique_customers,
        ROW_NUMBER() OVER (ORDER BY DATE(o.order_date)) as day_sequence,
        SUM(SUM(o.total_amount)) OVER (ORDER BY DATE(o.order_date)) as running_total_revenue
    FROM orders o
    WHERE o.status != 'cancelled'
    GROUP BY DATE(o.order_date)
)
SELECT
    order_date,
    order_count,
    daily_revenue,
    avg_order_value,
    unique_customers,
    day_sequence,
    running_total_revenue
FROM daily_sales
ORDER BY order_date DESC;

-- QUERY 7: Order Summary Statistics
-- Basic aggregations for dashboard
-- =============================================================================
SELECT
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value,
    MIN(o.total_amount) as min_order_value,
    MAX(o.total_amount) as max_order_value,
    SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
    SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) as pending_orders,
    SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_orders
FROM orders o;

-- QUERY 8: Customer Order Frequency Analysis
-- Identifies most valuable and frequent customers
-- =============================================================================
WITH customer_frequency AS (
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        COUNT(o.id) as order_frequency,
        SUM(o.total_amount) as customer_lifetime_value,
        AVG(o.total_amount) as avg_order_value,
        PERCENT_RANK() OVER (ORDER BY COUNT(o.id)) as frequency_percentile,
        PERCENT_RANK() OVER (ORDER BY SUM(o.total_amount)) as value_percentile
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
    GROUP BY c.id, c.first_name, c.last_name, c.email
)
SELECT
    id,
    CONCAT(first_name, ' ', last_name) as customer_name,
    email,
    order_frequency,
    COALESCE(customer_lifetime_value, 0) as customer_lifetime_value,
    COALESCE(avg_order_value, 0) as avg_order_value,
    ROUND(frequency_percentile * 100, 2) as frequency_percentile,
    ROUND(value_percentile * 100, 2) as value_percentile
FROM customer_frequency
ORDER BY customer_lifetime_value DESC;

-- =============================================================================
-- PERFORMANCE NOTES
-- =============================================================================
/*
INDEXES USED:
- idx_orders_customer_id: Fast lookup for customer orders
- idx_products_metadata_gin: JSONB metadata searches
- idx_order_items_product_id: Product sales aggregation
- idx_order_items_order_id: Order item lookups

WINDOW FUNCTIONS:
- RANK(): Handles ties by skipping ranks
- DENSE_RANK(): Handles ties without skipping ranks
- ROW_NUMBER(): Unique number for each row
- SUM() OVER (ORDER BY ...): Running totals
- PERCENT_RANK(): Relative ranking as percentage

COMMON TABLE EXPRESSIONS (CTEs):
- Improves query readability
- Allows reuse of common logic
- Optimizer can materialize or inline CTEs

JSONB OPERATORS:
- '->': Get value as JSON
- '->>': Get value as text
- '@>': Contains (full text search)
- '?': Key exists
*/

