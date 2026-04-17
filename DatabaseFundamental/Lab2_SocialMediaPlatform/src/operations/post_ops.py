import json
from datetime import datetime
from src.db.postgres import get_connection, release_connection
from src.models.schemas import Post

def create_post(post: Post) -> Post:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO posts (user_id, content, metadata)
                VALUES (%s, %s, %s)
                RETURNING id, created_at, updated_at
            """, (post.user_id, post.content, json.dumps(post.metadata)))
            
            result = cur.fetchone()
            post.id = result[0]
            post.created_at = result[1]
            post.updated_at = result[2]
            
            conn.commit()
            return post
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)

def get_post(post_id: int) -> Post:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, user_id, content, metadata, created_at, updated_at
                FROM posts WHERE id = %s
            """, (post_id,))
            
            row = cur.fetchone()
            if row:
                return Post(id=row[0], user_id=row[1], content=row[2], 
                         metadata=row[3], created_at=row[4], updated_at=row[5])
            return None
    finally:
        release_connection(conn)
