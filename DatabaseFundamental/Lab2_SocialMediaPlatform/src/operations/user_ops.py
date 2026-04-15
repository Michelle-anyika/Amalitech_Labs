from src.db.postgres import get_connection, release_connection
from src.models.schemas import User

def create_user(user: User) -> User:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, full_name, bio)
                VALUES (%s, %s, %s, %s)
                RETURNING id, follower_count, following_count, created_at, updated_at
            """, (user.username, user.email, user.full_name, user.bio))
            
            result = cur.fetchone()
            user.id = result[0]
            user.follower_count = result[1]
            user.following_count = result[2]
            user.created_at = result[3]
            user.updated_at = result[4]
            
            conn.commit()
            return user
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)

def get_user(user_id: int) -> User:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, full_name, bio, follower_count, following_count, created_at, updated_at
                FROM users WHERE id = %s
            """, (user_id,))
            
            row = cur.fetchone()
            if row:
                return User(id=row[0], username=row[1], email=row[2], full_name=row[3], 
                         bio=row[4], follower_count=row[5], following_count=row[6], 
                         created_at=row[7], updated_at=row[8])
            return None
    finally:
        release_connection(conn)
