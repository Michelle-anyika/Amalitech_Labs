# Lab 2: Social Media Platform - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### 1. Navigate to Lab 2
```bash
cd DatabaseFundamental/Lab2_SocialMediaPlatform
```

### 2. Setup Environment
```bash
cp .env.example .env
```

### 3. Start Services
```bash
docker-compose up -d

# Verify services are running
docker-compose ps
```

Should see:
- social_media_postgres ✓ Up
- social_media_redis ✓ Up
- social_media_mongodb ✓ Up

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Populate Sample Data
```bash
python src/scripts/populate_db.py
```

Creates:
- 10 users
- 20 posts with metadata
- 15 follows relationships
- 30 comments

### 6. Run Tests
```bash
pytest tests/ -v
```

### 7. Generate User Feed
```python
python

from src.operations.feed_ops import feed_ops

# Get user's feed
feed = feed_ops.get_user_feed(user_id=1, limit=10)
print(f"Got {len(feed)} posts in feed")

# Check cache stats
print(feed_ops.get_cache_stats())
```

## 📊 Quick Operations

### Create a Post
```python
from src.operations.post_ops import post_ops

post_id = post_ops.create_post(
    user_id=1,
    content="Hello social media!",
    metadata={
        "tags": ["intro", "welcome"],
        "location": "San Francisco"
    }
)
```

### Follow a User (Transactional)
```python
from src.operations.follow_ops import follow_ops

follow_ops.follow_user(
    follower_id=1,
    following_id=2
)
# ✅ Both follower counts updated atomically
```

### Get User's Timeline
```python
from src.operations.feed_ops import feed_ops

feed = feed_ops.get_user_feed(user_id=1, limit=20, offset=0)
for post in feed:
    print(f"{post['author']} posted: {post['content']}")
```

## 🔧 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f postgres

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
docker-compose up -d
```

## 📚 Key Files

- **src/operations/feed_ops.py** - Feed generation (complex CTEs)
- **src/operations/follow_ops.py** - Transactional follow logic
- **sql/queries.sql** - Complex feed queries
- **sql/schema.sql** - Database structure
- **tests/test_feed.py** - Feed optimization tests

## ⚙️ Environment Variables

In `.env`:
```
POSTGRES_PORT=5433        (Note: different from Lab1!)
REDIS_PORT=6380
MONGODB_PORT=27018
```

## 🐛 Troubleshooting

**PostgreSQL connection refused?**
```bash
docker-compose ps          # Check if running
docker-compose logs postgres  # Check logs
```

**Tests failing?**
```bash
# Clear cache
docker-compose down -v
docker-compose up -d

# Repopulate
python src/scripts/populate_db.py
```

## 📝 Next Steps

1. Review `docs/ER_DIAGRAM.md` - Understand the schema
2. Review `docs/SCHEMA_DESIGN.md` - Learn design decisions
3. Review `sql/queries.sql` - Study feed query
4. Run `pytest tests/ -v` - See all operations work
5. Modify sample data - Experiment with queries

## 💡 Lab 2 Focus Areas

- **Transactional Operations** - Follow user atomically
- **Complex Queries** - Feed with CTEs and window functions
- **Cache Strategy** - Redis for timeline caching
- **Activity Logging** - MongoDB for event tracking
- **Query Optimization** - Index strategy for high-read workload

---

**All set!** Start with Step 1 above. Questions? Check README.md 🚀

