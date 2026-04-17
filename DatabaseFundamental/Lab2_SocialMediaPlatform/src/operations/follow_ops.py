from datetime import datetime
from src.db.postgres import get_connection, release_connection
from src.db.mongodb_client import get_mongodb

def follow_user(follower_id: int, following_id: int) -> bool:
    """
    Transactional follow operation.
    Updates the followers table, and denormalized counters on the users table.
    Also logs the activity in MongoDB.
    """
    if follower_id == following_id:
        raise ValueError("User cannot follow themselves")
        
    conn = get_connection()
    mongo = get_mongodb()
    
    try:
        with conn.cursor() as cur:
            # 1. Insert into followers table
            cur.execute("""
                INSERT INTO followers (follower_id, following_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING 1
            """, (follower_id, following_id))
            
            inserted = cur.fetchone()
            if not inserted:
                # Already following
                return False
                
            # 2. Update follower_count for the user being followed
            cur.execute("""
                UPDATE users SET follower_count = follower_count + 1
                WHERE id = %s
            """, (following_id,))
            
            # 3. Update following_count for the user who is following
            cur.execute("""
                UPDATE users SET following_count = following_count + 1
                WHERE id = %s
            """, (follower_id,))
            
            conn.commit()
            
            # Log to MongoDB (outside the Postgres transaction, but part of the logical operation)
            try:
                mongo.activity_stream.insert_one({
                    "user_id": follower_id,
                    "action": "FOLLOW",
                    "target_user_id": following_id,
                    "created_at": datetime.utcnow()
                })
            except Exception as mongo_err:
                # Log the error but don't fail the pg transaction since it succeeded
                print(f"MongoDB logging failed: {mongo_err}")
                
            return True
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)

def unfollow_user(follower_id: int, following_id: int) -> bool:
    conn = get_connection()
    mongo = get_mongodb()
    
    try:
        with conn.cursor() as cur:
            # 1. Delete from followers table
            cur.execute("""
                DELETE FROM followers
                WHERE follower_id = %s AND following_id = %s
                RETURNING 1
            """, (follower_id, following_id))
            
            deleted = cur.fetchone()
            if not deleted:
                return False
                
            # 2. Update follower_count
            cur.execute("""
                UPDATE users SET follower_count = GREATEST(follower_count - 1, 0)
                WHERE id = %s
            """, (following_id,))
            
            # 3. Update following_count
            cur.execute("""
                UPDATE users SET following_count = GREATEST(following_count - 1, 0)
                WHERE id = %s
            """, (follower_id,))
            
            conn.commit()
            
            try:
                mongo.activity_stream.insert_one({
                    "user_id": follower_id,
                    "action": "UNFOLLOW",
                    "target_user_id": following_id,
                    "created_at": datetime.utcnow()
                })
            except Exception as mongo_err:
                print(f"MongoDB logging failed: {mongo_err}")
                
            return True
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)
