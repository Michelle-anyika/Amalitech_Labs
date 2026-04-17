import json
from typing import List
from src.db.postgres import get_connection, release_connection
from src.db.redis_client import get_redis_client
from src.models.schemas import FeedItem

CACHE_TTL = 3600  # 1 hour

def generate_user_feed(user_id: int, page: int = 1, page_size: int = 20) -> List[FeedItem]:
    """
    Generates a feed of posts from users that the current user is following.
    Uses Redis cache first. If empty, falls back to Postgres query with CTEs and Window Functions.
    """
    redis_client = get_redis_client()
    cache_key = f"user_feed:{user_id}:page:{page}"
    
    # Try getting from cache
    try:
        cached_feed = redis_client.get(cache_key)
        if cached_feed:
            feed_data = json.loads(cached_feed)
            return [FeedItem(**item) for item in feed_data]
    except Exception as e:
        print(f"Redis error: {e}")
        
    # If not in cache, query Postgres
    conn = get_connection()
    try:
        # Complex Feed Query using CTE, Window Function (ROW_NUMBER) and JOIN
        # 1. Finds all users the user is following
        # 2. Grabs posts from those people
        # 3. Uses ROW_NUMBER to rank posts by created_at date
        # 4. Filters to only the posts for the specific page
        query = """
        WITH following_users AS (
            SELECT following_id 
            FROM followers 
            WHERE follower_id = %s
        ),
        ranked_posts AS (
            SELECT 
                p.id as post_id, 
                p.user_id as author_id,
                u.username as author_username,
                p.content, 
                p.metadata, 
                p.created_at,
                ROW_NUMBER() OVER(ORDER BY p.created_at DESC) as rank
            FROM posts p
            JOIN following_users f ON p.user_id = f.following_id
            JOIN users u ON u.id = p.user_id
        )
        SELECT post_id, author_id, author_username, content, metadata, created_at, rank
        FROM ranked_posts
        WHERE rank > %s AND rank <= %s
        ORDER BY rank
        """
        
        offset = (page - 1) * page_size
        limit_rank = offset + page_size
        
        feed = []
        feed_dicts = []
        with conn.cursor() as cur:
            cur.execute(query, (user_id, offset, limit_rank))
            rows = cur.fetchall()
            
            for row in rows:
                item = FeedItem(
                    post_id=row[0],
                    author_id=row[1],
                    author_username=row[2],
                    content=row[3],
                    metadata=row[4],
                    created_at=row[5],
                    rank=row[6]
                )
                feed.append(item)
                
                # prepare dictionary for caching (handling datetime)
                item_dict = {
                    "post_id": item.post_id,
                    "author_id": item.author_id,
                    "author_username": item.author_username,
                    "content": item.content,
                    "metadata": item.metadata,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "rank": item.rank
                }
                feed_dicts.append(item_dict)
                
        # Cache the result
        try:
            if feed_dicts:
                redis_client.setex(cache_key, CACHE_TTL, json.dumps(feed_dicts))
        except Exception as e:
            print(f"Redis caching error: {e}")
            
        return feed
    finally:
        release_connection(conn)

def clear_user_feed_cache(user_id: int):
    redis_client = get_redis_client()
    try:
        keys = redis_client.keys(f"user_feed:{user_id}:page:*")
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Redis cache clearing error: {e}")
