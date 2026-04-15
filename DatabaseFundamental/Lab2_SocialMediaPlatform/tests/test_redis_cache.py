def test_redis_connection():
    from src.db.redis_client import get_redis_client
    
    redis_client = get_redis_client()
    assert redis_client.ping() is True
    
def test_redis_set_get():
    from src.db.redis_client import get_redis_client
    
    redis_client = get_redis_client()
    redis_client.set("test_key", "test_value")
    val = redis_client.get("test_key")
    assert val == "test_value"
    redis_client.delete("test_key")
