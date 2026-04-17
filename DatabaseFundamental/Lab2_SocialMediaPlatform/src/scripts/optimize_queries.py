import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.db.postgres import get_connection, release_connection
from src.operations.feed_ops import generate_user_feed

def test_explain_analyze(user_id):
    query = """
    EXPLAIN ANALYZE
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
    WHERE rank > 0 AND rank <= 20
    ORDER BY rank
    """
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            print("\n================== FEED QUERY EXPLAIN ANALYZE ==================")
            cur.execute(query, (user_id,))
            rows = cur.fetchall()
            for r in rows:
                print(r[0])
            print("================================================================\n")
    finally:
        release_connection(conn)

def demo_redis_cache():
    print("Testing Feed Retrieval Time with Redis Cache...")
    
    # First call will hit Postgres (assuming not cached or we passed a new user/page)
    start_time = time.time()
    feed = generate_user_feed(user_id=1, page=1)
    db_time = time.time() - start_time
    print(f"Time to generate from Postgres: {db_time:.5f} seconds ({len(feed)} items)")
    
    # Second call should hit Redis cache
    start_time = time.time()
    feed_cached = generate_user_feed(user_id=1, page=1)
    cache_time = time.time() - start_time
    print(f"Time to retrieve from Redis: {cache_time:.5f} seconds ({len(feed_cached)} items)")

if __name__ == "__main__":
    test_explain_analyze(user_id=1)
    demo_redis_cache()
