import time
from src.models.schemas import User, Post
from src.operations.user_ops import create_user, get_user
from src.operations.post_ops import create_post, get_post
from src.operations.follow_ops import follow_user, unfollow_user

def test_user_creation():
    timestamp = int(time.time())
    u = User(username=f"testuser_{timestamp}", email=f"test_{timestamp}@example.com")
    created = create_user(u)
    assert created.id is not None
    assert created.username == f"testuser_{timestamp}"

def test_post_creation():
    timestamp = int(time.time())
    u = User(username=f"postuser_{timestamp}", email=f"post_{timestamp}@example.com")
    created_u = create_user(u)
    
    p = Post(user_id=created_u.id, content="This is a test post", metadata={"type": "test"})
    created_p = create_post(p)
    assert created_p.id is not None
    assert created_p.user_id == created_u.id

def test_atomic_follow_transaction():
    timestamp = int(time.time())
    u1 = create_user(User(username=f"u1_{timestamp}", email=f"u1_{timestamp}@ex.com"))
    u2 = create_user(User(username=f"u2_{timestamp}", email=f"u2_{timestamp}@ex.com"))
    
    assert u1.following_count == 0
    assert u2.follower_count == 0
    
    # u1 follows u2
    success = follow_user(u1.id, u2.id)
    assert success is True
    
    # Verify counts were updated properly in DB
    u1_db = get_user(u1.id)
    u2_db = get_user(u2.id)
    
    assert u1_db.following_count == 1
    assert u2_db.follower_count == 1
    
    # Test Unfollow
    unfollow_success = unfollow_user(u1.id, u2.id)
    assert unfollow_success is True
    
    u1_db_after = get_user(u1.id)
    u2_db_after = get_user(u2.id)
    
    assert u1_db_after.following_count == 0
    assert u2_db_after.follower_count == 0
