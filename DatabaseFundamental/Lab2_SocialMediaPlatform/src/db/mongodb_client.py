from pymongo import MongoClient
import logging
from src.config.settings import MONGO_URI, MONGO_DB

logger = logging.getLogger(__name__)

class MongoDBClient:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._client is None:
            try:
                cls._client = MongoClient(MONGO_URI)
                cls._db = cls._client[MONGO_DB]
            except Exception as e:
                logger.error(f"Error connecting to MongoDB: {e}")
                raise e
        return cls._db

def get_mongodb():
    return MongoDBClient.get_db()
