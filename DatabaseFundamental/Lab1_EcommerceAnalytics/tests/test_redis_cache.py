"""
Tests for Redis caching operations
"""
import pytest
from src.db.redis_client import redis_client


class TestRedisCaching:
    """Test Redis cache operations"""

    def test_set_and_get(self, cleanup_redis):
        """Test setting and getting a value"""
        redis_client.set("test_key", {"name": "test", "value": 123})
        value = redis_client.get("test_key")

        assert value is not None
        assert value["name"] == "test"
        assert value["value"] == 123

    def test_set_with_expiration(self, cleanup_redis):
        """Test setting a value with expiration"""
        redis_client.set("expire_key", "test_value", expire_seconds=10)

        assert redis_client.exists("expire_key") is True
        ttl = redis_client.get_ttl("expire_key")
        assert ttl > 0
        assert ttl <= 10

    def test_exists(self, cleanup_redis):
        """Test key existence check"""
        redis_client.set("exist_key", "value")

        assert redis_client.exists("exist_key") is True
        assert redis_client.exists("nonexistent_key") is False

    def test_delete(self, cleanup_redis):
        """Test deleting a key"""
        redis_client.set("delete_key", "value")
        assert redis_client.exists("delete_key") is True

        redis_client.delete("delete_key")
        assert redis_client.exists("delete_key") is False

    def test_increment(self, cleanup_redis):
        """Test incrementing a numeric value"""
        redis_client.set("counter", 0)

        result = redis_client.increment("counter", 5)
        assert result == 5

        result = redis_client.increment("counter", 3)
        assert result == 8

    def test_decrement(self, cleanup_redis):
        """Test decrementing a numeric value"""
        redis_client.set("counter", 10)

        result = redis_client.decrement("counter", 3)
        assert result == 7

    def test_cache_miss(self, cleanup_redis):
        """Test getting a non-existent key"""
        value = redis_client.get("nonexistent")
        assert value is None

    def test_json_serialization(self, cleanup_redis):
        """Test JSON serialization of complex objects"""
        data = {
            "products": [
                {"id": 1, "name": "Product 1", "price": 29.99},
                {"id": 2, "name": "Product 2", "price": 49.99}
            ],
            "total": 79.98
        }

        redis_client.set("products", data)
        retrieved = redis_client.get("products")

        assert retrieved == data
        assert len(retrieved["products"]) == 2
        assert retrieved["total"] == 79.98

