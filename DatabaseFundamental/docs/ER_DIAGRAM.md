# Entity-Relationship Diagram (ER Diagram)

## E-Commerce Database Schema

```
┌──────────────────────────────────────────────────────────────────────┐
│                    E-COMMERCE DATABASE SCHEMA                         │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌──────────────────┐
│    CATEGORIES       │         │    PRODUCTS      │
├─────────────────────┤         ├──────────────────┤
│ id (PK)             │◄────────│ id (PK)          │
│ name                │ (1:N)   │ name             │
│ description         │         │ category_id (FK) │
│ created_at          │         │ price            │
│ updated_at          │         │ stock_quantity   │
└─────────────────────┘         │ description      │
                                │ metadata (JSONB) │ ◄─── GIN Index
                                │ created_at       │
                                │ updated_at       │
                                └──────────────────┘
                                        ▲
                                        │ (1:N)
                                        │
                    ┌───────────────────┴────────────────────┐
                    │                                        │
            ┌──────────────────┐                   ┌─────────────────┐
            │  ORDER_ITEMS     │                   │   CUSTOMERS     │
            ├──────────────────┤                   ├─────────────────┤
            │ id (PK)          │                   │ id (PK)         │
            │ order_id (FK)    │───┐       ┌──────│ first_name      │
            │ product_id (FK)  │◄──┤───┐   │      │ last_name       │
            │ quantity         │   │   │   │      │ email (UNIQUE)  │
            │ unit_price       │   │   │   │      │ phone           │
            │ subtotal         │   │   │   │      │ address         │
            │ created_at       │   │   │   │      │ city            │
            └──────────────────┘   │   │   │      │ country         │
                                   │   │   │      │ created_at      │
                            ┌──────┴──┐│   │      │ updated_at      │
                            │ ORDERS  ││   │      └─────────────────┘
                            ├─────────┤│   │              ▲
                            │ id (PK) ││   │              │ (1:N)
                            │ customer_id (FK)────────────┘
                            │ order_date │   B-tree Index
                            │ total_amount   idx_orders_customer_id
                            │ status      │
                            │ created_at  │
                            │ updated_at  │
                            └─────────────┘
                                    │
                                    │ (1:N)
                                    │
                    ┌───────────────┴─────────────────┐
                    │                                 │
            ┌──────────────────────────────────────┐
            │   ORDER_STATUS_HISTORY               │
            ├──────────────────────────────────────┤
            │ id (PK)                              │
            │ order_id (FK)                        │
            │ status                               │
            │ changed_at                           │
            │ notes                                │
            └──────────────────────────────────────┘
```

## Table Relationships

### One-to-Many (1:N) Relationships

1. **CATEGORIES → PRODUCTS**
   - One category has many products
   - Foreign Key: `products.category_id` → `categories.id`
   - Constraint: ON DELETE RESTRICT (prevent deletion of categories with products)

2. **CUSTOMERS → ORDERS**
   - One customer has many orders
   - Foreign Key: `orders.customer_id` → `customers.id`
   - Constraint: ON DELETE CASCADE (delete orders when customer is deleted)
   - Index: `idx_orders_customer_id` (B-tree) for fast customer lookup

3. **ORDERS → ORDER_ITEMS**
   - One order has many line items
   - Foreign Key: `order_items.order_id` → `orders.id`
   - Constraint: ON DELETE CASCADE

4. **PRODUCTS → ORDER_ITEMS**
   - One product appears in many orders
   - Foreign Key: `order_items.product_id` → `products.id`
   - Constraint: ON DELETE RESTRICT (prevent deletion of purchased products)

5. **ORDERS → ORDER_STATUS_HISTORY**
   - One order has many status changes
   - Foreign Key: `order_status_history.order_id` → `orders.id`
   - Constraint: ON DELETE CASCADE

## Key Indexes

| Index Name | Table | Columns | Type | Purpose |
|------------|-------|---------|------|---------|
| idx_orders_customer_id | orders | customer_id | B-tree | Fast lookup of customer orders |
| idx_orders_customer_created | orders | (customer_id, created_at) | B-tree | Composite query optimization |
| idx_orders_status | orders | status | B-tree | Filter orders by status |
| idx_products_metadata_gin | products | metadata | GIN | JSONB metadata searches |
| idx_products_category | products | category_id | B-tree | Find products in category |
| idx_customers_email | customers | email | B-tree | Fast email lookup |
| idx_order_status_history_order | order_status_history | order_id | B-tree | Audit trail queries |

## Special Features

### JSONB Metadata in Products
The `products.metadata` column stores flexible attributes as JSON:

```json
{
  "brand": "TechBrand",
  "processor": "Intel i7",
  "ram": "16GB",
  "colors": ["silver", "black"],
  "sizes": ["S", "M", "L", "XL"],
  "material": "100% cotton"
}
```

**GIN Index** enables efficient queries:
```sql
WHERE metadata->>'color' = 'red'
WHERE metadata @> '{"brand": "Nike"}'
```

## Normalization

### First Normal Form (1NF)
- ✅ All attributes contain atomic values
- ✅ No repeating groups
- ✅ Each attribute has a single value per row

### Second Normal Form (2NF)
- ✅ Meets 1NF requirements
- ✅ All non-key attributes depend on the entire primary key
- ✅ No partial dependencies

### Third Normal Form (3NF)
- ✅ Meets 2NF requirements
- ✅ No transitive dependencies
- ✅ Non-key attributes depend only on primary keys

**Example of 3NF compliance:**
- `ORDER_ITEMS.subtotal` = `quantity × unit_price` (denormalized for performance)
- `ORDERS.total_amount` = calculated from order items (provides audit trail)
- This small denormalization is intentional for performance and historical accuracy


