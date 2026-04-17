import redis
import logging
from src.config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

logger = logging.getLogger(__name__)

class RedisClient:
    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            try:
                cls._instance = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=REDIS_DB,
                    decode_responses=True
                )
            except Exception as e:
                logger.error(f"Error connecting to Redis: {e}")
                raise e
        return cls._instance

def get_redis_client():
    return RedisClient.get_client()
