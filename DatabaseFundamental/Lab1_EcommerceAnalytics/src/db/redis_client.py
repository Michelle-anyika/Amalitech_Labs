"""
Redis caching client for storing and retrieving cached data
"""
import redis
import json
import logging
from typing import Any, Optional

from src.config.settings import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Client for Redis caching operations"""

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            self._init_connection()

    def _init_connection(self):
        """Initialize Redis connection"""
        try:
            self._connection = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            # Test connection
            self._connection.ping()
            logger.info("Redis connection established successfully")
        except redis.ConnectionError as error:
            logger.error(f"Error connecting to Redis: {error}")
            raise

    def set(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None
    ) -> bool:
        """
        Set a value in Redis

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expire_seconds: Optional expiration time in seconds

        Returns:
            True if successful
        """
        try:
            json_value = json.dumps(value)
            self._connection.set(key, json_value, ex=expire_seconds)
            logger.debug(f"Cached value for key: {key}")
            return True
        except Exception as error:
            logger.error(f"Error setting cache: {error}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            value = self._connection.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as error:
            logger.error(f"Error getting cache: {error}")
            return None

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        try:
            return self._connection.exists(key) > 0
        except Exception as error:
            logger.error(f"Error checking key existence: {error}")
            return False

    def delete(self, key: str) -> bool:
        """Delete a key from Redis"""
        try:
            self._connection.delete(key)
            logger.debug(f"Deleted cache key: {key}")
            return True
        except Exception as error:
            logger.error(f"Error deleting cache: {error}")
            return False

    def flush_all(self) -> bool:
        """Flush all data in Redis"""
        try:
            self._connection.flushdb()
            logger.warning("Flushed all Redis data")
            return True
        except Exception as error:
            logger.error(f"Error flushing Redis: {error}")
            return False

    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a numeric value in Redis"""
        try:
            return self._connection.incr(key, amount)
        except Exception as error:
            logger.error(f"Error incrementing value: {error}")
            return 0

    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement a numeric value in Redis"""
        try:
            return self._connection.decr(key, amount)
        except Exception as error:
            logger.error(f"Error decrementing value: {error}")
            return 0

    def get_ttl(self, key: str) -> int:
        """Get time-to-live for a key in seconds"""
        try:
            return self._connection.ttl(key)
        except Exception as error:
            logger.error(f"Error getting TTL: {error}")
            return -1

    def close(self):
        """Close Redis connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Redis connection closed")


# Singleton instance
redis_client = RedisClient()

