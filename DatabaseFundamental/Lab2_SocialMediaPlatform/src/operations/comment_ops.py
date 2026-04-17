from src.db.postgres import get_connection, release_connection
from src.models.schemas import Comment

def create_comment(comment: Comment) -> Comment:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO comments (post_id, user_id, content)
                VALUES (%s, %s, %s)
                RETURNING id, created_at, updated_at
            """, (comment.post_id, comment.user_id, comment.content))
            
            result = cur.fetchone()
            comment.id = result[0]
            comment.created_at = result[1]
            comment.updated_at = result[2]
            
            conn.commit()
            return comment
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)
