import time
from src.models.schemas import User, Post
from src.operations.user_ops import create_user
from src.operations.post_ops import create_post
from src.operations.follow_ops import follow_user
from src.operations.feed_ops import generate_user_feed, clear_user_feed_cache

def test_feed_generation():
    timestamp = int(time.time())
    
    u1 = create_user(User(username=f"fu1_{timestamp}", email=f"fu1_{timestamp}@ex.com"))
    u2 = create_user(User(username=f"fu2_{timestamp}", email=f"fu2_{timestamp}@ex.com"))
    
    # u1 follows u2
    follow_user(u1.id, u2.id)
    
    # u2 makes a post
    create_post(Post(user_id=u2.id, content="Feed testing 123", metadata={}))
    
    # Clear cache before testing
    clear_user_feed_cache(u1.id)
    
    # Generate Feed for u1
    feed = generate_user_feed(u1.id)
    assert len(feed) > 0
    assert any(item.content == "Feed testing 123" for item in feed)
