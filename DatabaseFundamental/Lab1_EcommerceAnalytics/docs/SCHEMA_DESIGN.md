# Schema Design and Normalization Documentation

## Design Rationale

The e-commerce database schema is designed to support a complete order management system with integrated analytics, caching, and session management. The design follows relational best practices while pragmatically using PostgreSQL's advanced features for performance and flexibility.

## Normalization Decisions

### First Normal Form (1NF)
**Principle**: All table attributes must contain only atomic (indivisible) values.

**Implementation**:
- `order_items` table is separated from `orders` to avoid repeating groups
- `order_status_history` tracks all status changes instead of storing them in `orders`
- Each attribute contains a single value, no arrays or nested structures (except JSONB metadata which is intentional)

### Second Normal Form (2NF)
**Principle**: All non-key attributes must depend on the entire primary key, not just part of it.

**Implementation**:
- `order_items` has a composite relationship with both order and product
- All attributes in `order_items` depend on the combination of `order_id` AND `product_id`
- `subtotal` correctly depends on both the order and the specific product line item

### Third Normal Form (3NF)
**Principle**: Non-key attributes must depend only on the primary key, not on other non-key attributes.

**Implementation**:
- `categories` is separate from `products` (product properties shouldn't be intertwined with category properties)
- `customers` data is independent of `orders` data
- No transitive dependencies exist

### Intentional Denormalization

We've made strategic denormalization decisions for valid reasons:

#### 1. **Order Totals**
```sql
-- DENORMALIZED: orders.total_amount
-- Can be calculated from: SUM(order_items.subtotal)
```

**Rationale**:
- Provides historical accuracy (prices at time of order)
- Faster query performance for reporting
- Single source of truth for order value
- Prevents recalculation errors

#### 2. **JSONB Metadata**
```sql
-- products.metadata JSONB column
```

**Rationale**:
- Avoids schema explosion (different products need different attributes)
- Electronics need: processor, RAM, storage
- Clothing needs: sizes, colors, materials
- Books need: author, pages, ISBN
- Solves the problem of semi-structured data without creating many nullable columns
- GIN index provides efficient searches

#### 3. **Order Item Subtotals**
```sql
-- DENORMALIZED: order_items.subtotal
-- Can be calculated from: quantity * unit_price
```

**Rationale**:
- Prevents arithmetic during queries
- Historical record (prices change)
- Audit trail

## Table Design Details

### CUSTOMERS Table
- **Primary Key**: `id` (surrogate key)
- **Unique Constraint**: `email`
- **Check Constraints**: Email format validation
- **Indexes**:
  - `email` - for login/lookup
  - `city` - for geographic analysis

**Design Choice**: Surrogate key (auto-increment ID) instead of email as primary key because:
- Email can change
- Provides stable foreign key reference
- Improves query performance

### PRODUCTS Table
- **Primary Key**: `id` (surrogate key)
- **Foreign Key**: `category_id` → `categories`
- **JSONB Column**: `metadata` - flexible schema
- **Indexes**:
  - `idx_products_category` (B-tree) - find products in category
  - `idx_products_name` (B-tree) - text search
  - `idx_products_metadata_gin` (GIN) - JSONB queries

**JSONB Design**:
```sql
-- Example metadata for different products:

-- Electronics
{"brand": "Apple", "processor": "M1", "ram": "8GB", "colors": ["silver", "black"]}

-- Clothing
{"material": "100% cotton", "sizes": ["S", "M", "L"], "colors": ["red", "blue"]}

-- Books
{"author": "John Doe", "pages": 500, "isbn": "123-456", "format": ["hardcover", "ebook"]}
```

### ORDERS Table
- **Primary Key**: `id` (surrogate key)
- **Foreign Key**: `customer_id` → `customers`
- **Status Enumeration**: pending, confirmed, shipped, delivered, cancelled
- **Indexes**:
  - `idx_orders_customer_id` (B-tree) - **Critical for performance**
  - `idx_orders_customer_created` (composite B-tree) - recent customer orders
  - `idx_orders_status` (B-tree) - status filtering

**Index Strategy**:
- `idx_orders_customer_id` is essential because:
  - Most queries need "get all orders for customer"
  - Used in analytics (customer lifetime value)
  - Used in transaction processing
  - B-tree is optimal for range and equality queries

### ORDER_ITEMS Table
- **Primary Key**: `id` (surrogate key)
- **Foreign Keys**: `order_id` → `orders`, `product_id` → `products`
- **Composite Key Alternative**: Could use (order_id, product_id), but surrogate key preferred for:
  - Simplifies foreign key references
  - Better performance in some queries
  - Easier for auto-generated IDs

### ORDER_STATUS_HISTORY Table
- **Audit Trail**: Records every status change
- **Immutable**: Records are never updated, only inserted
- **Uses**: Order tracking, analytics, customer communication
- **Index**: `order_id` for quick lookup of order history

**Design Choice**: Separate table instead of JSON array because:
- Easier to query with SQL
- Each status change is a distinct event
- Better for audit compliance
- Natural time-series structure

## Constraints and Referential Integrity

### Foreign Key Constraints

| Constraint | From | To | On Delete | Rationale |
|-----------|------|----|-----------|----|
| fk_category | products.category_id | categories.id | RESTRICT | Prevent orphaned products |
| fk_customer | orders.customer_id | customers.id | CASCADE | Clean up when customer deleted |
| fk_order | order_items.order_id | orders.id | CASCADE | Clean up when order deleted |
| fk_product | order_items.product_id | products.id | RESTRICT | Prevent deleting purchased products |
| fk_order_history | order_status_history.order_id | orders.id | CASCADE | Clean up order history |

### Check Constraints

```sql
-- Prices and quantities
CHECK (price >= 0)
CHECK (stock_quantity >= 0)
CHECK (total_amount >= 0)

-- Non-empty strings
CHECK (name != '')
CHECK (first_name != '')
CHECK (last_name != '')

-- Email format
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
```

## Views for Analytics

### v_customer_order_summary
```sql
SELECT 
    customer_id, customer_name, email,
    total_orders, lifetime_value, avg_order_value,
    last_order_date
FROM v_customer_order_summary
ORDER BY lifetime_value DESC;
```

**Use Cases**:
- VIP customer identification
- Churn analysis
- Lifetime value reports

### v_product_sales
```sql
SELECT 
    id, name, category,
    total_items_sold, total_quantity, total_revenue,
    avg_price
FROM v_product_sales
ORDER BY total_revenue DESC;
```

**Use Cases**:
- Top seller identification
- Category performance
- Inventory decisions

## Performance Optimization Strategy

### Index Selection

**B-tree Indexes** (default, optimal for):
- Equality: `WHERE customer_id = 1`
- Range: `WHERE price BETWEEN 10 AND 100`
- Sorting: `ORDER BY created_at`

Applied to:
- Foreign keys (all)
- Frequently filtered columns (customer_id, status)
- Sorting columns (created_at, order_date)

**GIN Indexes** (optimal for):
- JSONB contains: `WHERE metadata @> '{"color": "red"}'`
- JSONB key access: `WHERE metadata->>'brand' = 'Nike'`

Applied to:
- `products.metadata` - complex product attributes

### Query Optimization Examples

**With Index (Fast)**:
```sql
-- Uses idx_orders_customer_id
SELECT * FROM orders WHERE customer_id = 1;
-- Execution time: < 1ms
```

**Without Index (Slow)**:
```sql
-- Would do full table scan
-- Execution time: 100ms+
```

**JSONB Query with GIN Index (Fast)**:
```sql
-- Uses idx_products_metadata_gin
SELECT * FROM products WHERE metadata->>'color' = 'red';
-- Execution time: < 5ms
```

## Scalability Considerations

### Current Design Supports

- **Millions of customers**: With proper indexing and partitioning
- **Billions of orders**: Partitioning by date recommended
- **Complex analytics**: Window functions, CTEs, aggregations
- **Real-time reporting**: Redis caching layer
- **Session management**: MongoDB for flexible structure
- **Flexible attributes**: JSONB for product variations

### Future Enhancements

1. **Partitioning**: Orders table by order_date (monthly/yearly)
2. **Materialized Views**: Pre-computed analytics results
3. **Read Replicas**: Separate analytics database
4. **Time-series DB**: For behavior tracking (InfluxDB, TimescaleDB)
5. **Full-text Search**: pg_trgm extension for product search

## Security Considerations

### Parameterized Queries
All Python functions use parameterized queries to prevent SQL injection:
```python
cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
```

### Column-level Permissions
- Can implement row-level security (RLS)
- Sensitive data (addresses) can be encrypted
- Audit trail via order_status_history

### GDPR Compliance
- Customer deletion cascades to orders (right to be forgotten)
- Audit trail maintained in order_status_history
- JSONB metadata doesn't contain sensitive data

