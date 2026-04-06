# DatabaseFundamental: E-Commerce Analytics Data Pipeline

## Project Overview

This is a comprehensive implementation of an **E-Commerce Analytics Data Pipeline** that demonstrates advanced database design, CRUD operations, NoSQL integration, and query optimization techniques.

## 🎯 Lab 1 Objectives

- [x] Design a normalized relational database schema for an e-commerce platform
- [x] Implement Python scripts using psycopg2 for transactional CRUD operations
- [x] Integrate NoSQL databases (Redis, MongoDB) with advanced SQL (JSONB)
- [x] Write complex SQL queries with window functions and CTEs
- [x] Analyze and optimize query performance using EXPLAIN ANALYZE and indexing

## 📋 Project Structure

```
DatabaseFundamental/
├── __init__.py                 # Package initialization
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker services setup
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Configuration management
│   ├── db/
│   │   ├── __init__.py
│   │   ├── postgres.py        # PostgreSQL connection & pooling
│   │   ├── redis_client.py    # Redis cache layer
│   │   └── mongodb_client.py  # MongoDB session storage
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Data models
│   ├── operations/
│   │   ├── __init__.py
│   │   ├── customer_ops.py    # Customer CRUD operations
│   │   ├── product_ops.py     # Product CRUD operations
│   │   ├── order_ops.py       # Order transactional operations
│   │   └── analytics.py       # Complex analytical queries
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py      # Data validation utilities
│   └── scripts/
│       ├── __init__.py
│       ├── populate_db.py     # Populate sample data
│       └── optimize_queries.py # Performance analysis
├── sql/
│   ├── schema.sql             # DDL: Table definitions
│   ├── sample_data.sql        # Sample data insertion
│   ├── indexes.sql            # Index creation
│   └── queries.sql            # Complex analytical queries
├── mongo/
│   └── init.js                # MongoDB initialization script
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_postgres_ops.py   # PostgreSQL operations tests
│   ├── test_redis_cache.py    # Redis cache tests
│   ├── test_mongodb_ops.py    # MongoDB operations tests
│   └── test_analytics.py      # Analytics queries tests
└── docs/
    ├── ER_DIAGRAM.md          # Entity-Relationship Diagram
    ├── SCHEMA_DESIGN.md       # Schema normalization documentation
    ├── OPTIMIZATION_REPORT.md # Performance optimization results
    └── API_REFERENCE.md       # API documentation
```

## 🗄️ Database Schema Overview

### PostgreSQL Tables

1. **customers** - Customer information with contact details
2. **products** - Product catalog with JSONB metadata
3. **categories** - Product categories
4. **orders** - Customer orders (transactional)
5. **order_items** - Line items in orders
6. **order_status_history** - Order status tracking

### Key Features

- **Normalization**: All tables follow 3rd Normal Form (3NF)
- **JSONB Support**: Product metadata stored as JSONB for flexibility
- **Constraints**: Primary keys, foreign keys, unique constraints
- **Transactions**: ACID-compliant order creation
- **Indexing**: B-tree and GIN indexes for performance

## 🔗 Integration Components

### PostgreSQL
- ACID transactions for order creation
- Window functions for ranking products by sales
- CTEs for complex aggregations
- JSONB for flexible product attributes

### Redis
- Caching layer for top 10 best-selling products
- Session data caching
- Real-time analytics updates

### MongoDB
- Unstructured session/shopping cart data
- User behavior tracking
- Flexible schema for varied data types

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Setup Instructions

1. **Clone the repository** and navigate to the branch:
```bash
git clone <repo-url>
cd Amalitech_Labs
git checkout lab1-ecommerce-analytics-pipeline
cd DatabaseFundamental
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start services using Docker**:
```bash
docker-compose up -d
```

4. **Verify services are healthy**:
```bash
docker-compose ps
```

5. **Initialize the database**:
```bash
python src/scripts/populate_db.py
```

6. **Run tests**:
```bash
pytest tests/ -v --cov=src
```

### Environment Variables

Create a `.env` file based on `.env.example`:
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_db
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password

REDIS_HOST=localhost
REDIS_PORT=6379

MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=admin
MONGODB_PASSWORD=admin_password
```

## 📊 Core Operations

### Customer Operations
- Create/Read/Update/Delete customers
- Retrieve customer order history
- Calculate customer lifetime value

### Product Operations
- Manage product catalog
- Add/update JSONB metadata (sizes, colors, specs)
- Track inventory and stock levels

### Order Operations
- Create orders transactionally
- Update order status
- Handle stock updates atomically

### Analytics Operations
- Rank products by sales volume (window functions)
- Calculate revenue per customer (CTEs)
- Generate sales reports with filters
- Find products by metadata attributes (GIN indexes)

## 📈 Performance Optimization

### Queries Analyzed
1. **Customer Order Queries** - Optimized with B-tree indexes
2. **Product Metadata Queries** - Optimized with GIN indexes
3. **Sales Ranking Queries** - Window function performance
4. **Revenue Aggregation** - CTE optimization

### EXPLAIN ANALYZE Results
See `docs/OPTIMIZATION_REPORT.md` for detailed before/after performance metrics.

### Key Indexes Applied
```sql
-- B-tree index on orders.customer_id
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- GIN index on products JSONB metadata
CREATE INDEX idx_products_metadata_gin ON products USING GIN(metadata);

-- Composite index for order queries
CREATE INDEX idx_orders_customer_created ON orders(customer_id, created_at);
```

## 📚 Documentation

- **ER Diagram**: `docs/ER_DIAGRAM.md` - Complete entity relationship model
- **Schema Design**: `docs/SCHEMA_DESIGN.md` - Normalization decisions and rationale
- **Optimization Report**: `docs/OPTIMIZATION_REPORT.md` - Performance analysis and improvements
- **API Reference**: `docs/API_REFERENCE.md` - Function signatures and usage examples

## ✅ Testing

Run the full test suite:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

Run specific test categories:
```bash
pytest tests/test_postgres_ops.py -v          # PostgreSQL operations
pytest tests/test_redis_cache.py -v           # Redis caching
pytest tests/test_mongodb_ops.py -v           # MongoDB sessions
pytest tests/test_analytics.py -v             # Analytics queries
```

## 🔒 Security Features

- **Parameterized Queries**: All SQL queries use parameterized statements to prevent SQL injection
- **Connection Pooling**: Efficient database connection management
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Input validation before database operations

## 📋 Milestones

- **Day 1**: Database Design and Setup ✓
  - ER diagram and DDL scripts
  - Docker PostgreSQL instance
  - Python database connection

- **Day 2**: Core Data Operations
  - CRUD operations for all entities
  - Transactional order creation
  - Sample data population

- **Day 3**: NoSQL Integration & Advanced SQL
  - Redis caching layer
  - MongoDB session storage
  - Complex queries with window functions and CTEs
  - JSONB metadata queries

- **Day 4**: Performance Tuning & Documentation
  - EXPLAIN ANALYZE on key queries
  - B-tree and GIN index optimization
  - Complete documentation

## 📝 SQL Files

- **sql/schema.sql** - All CREATE TABLE statements and constraints
- **sql/sample_data.sql** - Sample customer, product, and order data
- **sql/indexes.sql** - All index definitions
- **sql/queries.sql** - Complex analytical queries with explanations

## 🔧 Tools & Technologies

| Component | Technology | Version |
|-----------|-----------|---------|
| Database | PostgreSQL | 15 |
| Cache | Redis | 7 |
| NoSQL | MongoDB | 7 |
| ORM/Driver | psycopg2 | 2.9.9 |
| Python | Python | 3.11+ |
| Testing | pytest | 7.4.3 |

## 📄 License

This project is part of the Amalitech Labs curriculum.

## 👥 Author

Created as part of Amalitech's DatabaseFundamental curriculum - Lab 1.

---

**Note**: For detailed implementation examples and advanced usage, please refer to the source code and documentation files in the project structure.

