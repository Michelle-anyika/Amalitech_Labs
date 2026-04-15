# Lab 2: Social Media Platform Data Backend

## Project Overview

This lab implements a complete data backend for a **social media platform** with emphasis on:
- Complex relationship management (users, posts, followers)
- Transactional integrity (atomic follow operations)
- High-read optimization (feed generation)
- Multi-database integration (PostgreSQL, Redis, MongoDB)

## 🎯 Lab 2 Objectives

✅ Design normalized relational database schema for social media  
✅ Implement transactional operations (follow user atomically)  
✅ Combine SQL and NoSQL for different data types  
✅ Write complex feed queries (CTEs, JOINs, Window Functions)  
✅ Optimize query performance for high-read scenarios  

## 📋 Project Structure

```
Lab2_SocialMediaPlatform/
├── __init__.py
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker services setup
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
├── QUICK_START.md             # Setup guide
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Configuration management
│   ├── db/
│   │   ├── __init__.py
│   │   ├── postgres.py        # PostgreSQL connection & pooling
│   │   ├── redis_client.py    # Redis cache layer
│   │   └── mongodb_client.py  # MongoDB activity logging
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Data models
│   ├── operations/
│   │   ├── __init__.py
│   │   ├── user_ops.py        # User management
│   │   ├── post_ops.py        # Post operations
│   │   ├── follow_ops.py      # Follow operations (transactional)
│   │   ├── comment_ops.py     # Comment operations
│   │   └── feed_ops.py        # Feed generation & caching
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py      # Data validation
│   └── scripts/
│       ├── __init__.py
│       ├── populate_db.py     # Populate sample data
│       └── optimize_queries.py # Query optimization analysis
├── sql/
│   ├── schema.sql             # DDL: Table definitions
│   ├── sample_data.sql        # Sample data insertion
│   ├── indexes.sql            # Index creation
│   └── queries.sql            # Complex feed queries
├── mongo/
│   └── init.js                # MongoDB initialization
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_postgres_ops.py   # PostgreSQL operations
│   ├── test_redis_cache.py    # Redis cache tests
│   ├── test_mongodb_ops.py    # MongoDB activity logging
│   └── test_feed.py           # Feed generation tests
└── docs/
    ├── ER_DIAGRAM.md          # Entity-Relationship Diagram
    ├── SCHEMA_DESIGN.md       # Schema normalization documentation
    ├── OPTIMIZATION_REPORT.md # Performance optimization results
    └── FEED_DESIGN.md         # Feed algorithm documentation
```

## 🗄️ Database Schema Overview

### PostgreSQL Tables

1. **users** - User profiles with metadata
2. **posts** - User posts with JSONB metadata (tags, location)
3. **comments** - Comments on posts
4. **followers** - Follow relationships (join table)
5. **post_likes** - Post likes tracking
6. **comment_likes** - Comment likes tracking
7. **activity_log** - Basic activity audit trail

### Key Differences from Lab 1

- **Followers Table**: Bi-directional many-to-many relationship
- **Follow Transaction**: Atomic update of follower counts and follow records
- **Feed Query**: Complex CTE with JOINs and Window Functions
- **High-Read Focus**: Emphasis on cache and index optimization
- **JSONB Metadata**: Post attributes (tags, location, media URLs)

## 🔗 Integration Components

### PostgreSQL
- Normalized schema with 3NF
- Transactional follow operations (ACID)
- Complex feed query with CTEs
- Window functions for pagination
- Composite indexes for follower queries

### Redis
- Cached user timelines (hourly refresh)
- Follow count caching
- Feed pagination cache
- Activity feed precomputation

### MongoDB
- Activity stream (likes, follows, comments)
- User interaction logs
- Unstructured event data
- Time-series activity tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Setup Instructions

1. **Clone and navigate**:
```bash
cd DatabaseFundamental/Lab2_SocialMediaPlatform
```

2. **Create environment file**:
```bash
cp .env.example .env
```

3. **Start services**:
```bash
docker-compose up -d
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Populate sample data**:
```bash
python src/scripts/populate_db.py
```

6. **Run tests**:
```bash
pytest tests/ -v --cov=src
```

7. **Generate and optimize feed**:
```bash
python src/scripts/optimize_queries.py
```

## 📊 Core Operations

### User Operations
- Create/read/update user profiles
- Get user's followers
- Get user's following list
- Search users

### Post Operations
- Create posts with JSONB metadata
- Retrieve posts with author info
- Update/delete posts
- Search by metadata (tags, location)

### Follow Operations (Transactional)
- Follow user (updates 2 tables atomically)
- Unfollow user (atomic transaction)
- Check follow status
- Get follower/following counts

### Comment Operations
- Add comments to posts
- Get post comments
- Update/delete comments
- Like/unlike comments

### Feed Operations (Complex)
- Generate user's timeline
  - CTE for following relationships
  - JOIN with posts and authors
  - Window function for pagination (ROW_NUMBER)
- Cache timeline in Redis
- Retrieve paginated feed
- Clear cache on new posts

## 📈 Performance Focus

### Queries Optimized
1. **Follow User Query** - Atomic transaction
2. **Get User Feed** - CTE + JOINs + Window Functions
3. **Trending Posts** - Aggregation with likes/comments
4. **User Search** - Text index on usernames
5. **Activity Feed** - MongoDB time-series query

### Indexes Applied
- Composite B-tree on (user_id, created_at)
- B-tree on follower relationships
- B-tree on post creation date
- GIN index on JSONB metadata
- Text index on post content

## 📝 Documentation

- **ER Diagram**: Complete entity relationships
- **Schema Design**: Normalization decisions and rationale
- **Optimization Report**: Before/after EXPLAIN ANALYZE results
- **Feed Design**: Timeline algorithm explanation

## ✅ Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_feed.py -v

# With coverage report
pytest tests/ -v --cov=src --cov-report=html
```

## 🎯 Success Criteria

✅ Schema designed in 3NF with proper relationships  
✅ Follow operation is atomic (all-or-nothing)  
✅ Feed query uses CTEs and window functions  
✅ Redis caching reduces database load  
✅ MongoDB logs all user activities  
✅ Query performance optimized (target: <100ms for feed)  
✅ All tests passing (40+ test cases)  
✅ Complete documentation with ER diagrams  

## 📚 Technologies

| Component | Technology | Version |
|-----------|-----------|---------|
| Database | PostgreSQL | 15 |
| Cache | Redis | 7 |
| NoSQL | MongoDB | 7 |
| Driver | psycopg2 | 2.9.9 |
| Python | Python | 3.11+ |
| Testing | pytest | 7.4.3 |

## 🎓 Learning Outcomes

After completing Lab 2, you'll understand:
- Complex multi-table transaction design
- Feed algorithm optimization strategies
- Redis caching strategies for read-heavy workloads
- MongoDB for activity logging and time-series data
- Window functions for efficient pagination
- Query optimization with composite indexes

---

**Status**: Ready to develop  
**Branch**: `lab2-social-media-platform`  
**Last Updated**: April 6, 2026

