"""
MongoDB client for session and unstructured data storage
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from src.config.settings import settings

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Client for MongoDB operations"""

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._init_connection()

    def _init_connection(self):
        """Initialize MongoDB connection"""
        try:
            self._client = MongoClient(
                host=settings.MONGODB_HOST,
                port=settings.MONGODB_PORT,
                username=settings.MONGODB_USER,
                password=settings.MONGODB_PASSWORD,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[settings.MONGODB_DB]
            logger.info("MongoDB connection established successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as error:
            logger.error(f"Error connecting to MongoDB: {error}")
            raise

    def insert_session(self, user_id: int, session_data: Dict[str, Any]) -> Optional[str]:
        """
        Insert or update a user session

        Args:
            user_id: User ID
            session_data: Session data to store

        Returns:
            Inserted document ID
        """
        try:
            collection = self._db['sessions']
            session_doc = {
                'user_id': user_id,
                'data': session_data,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = collection.update_one(
                {'user_id': user_id},
                {'$set': session_doc},
                upsert=True
            )
            logger.info(f"Session stored for user {user_id}")
            return str(result.upserted_id) if result.upserted_id else str(user_id)
        except Exception as error:
            logger.error(f"Error inserting session: {error}")
            raise

    def get_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a user session

        Args:
            user_id: User ID

        Returns:
            Session data or None
        """
        try:
            collection = self._db['sessions']
            session = collection.find_one({'user_id': user_id})
            return session
        except Exception as error:
            logger.error(f"Error retrieving session: {error}")
            return None

    def insert_shopping_cart(
        self,
        user_id: int,
        cart_items: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Insert or update a shopping cart

        Args:
            user_id: User ID
            cart_items: List of cart items

        Returns:
            Cart document ID
        """
        try:
            collection = self._db['shopping_carts']
            cart_doc = {
                'user_id': user_id,
                'items': cart_items,
                'total_items': len(cart_items),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = collection.update_one(
                {'user_id': user_id},
                {'$set': cart_doc},
                upsert=True
            )
            logger.info(f"Cart stored for user {user_id}")
            return str(result.upserted_id) if result.upserted_id else str(user_id)
        except Exception as error:
            logger.error(f"Error inserting cart: {error}")
            raise

    def get_shopping_cart(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a user's shopping cart

        Args:
            user_id: User ID

        Returns:
            Cart data or None
        """
        try:
            collection = self._db['shopping_carts']
            cart = collection.find_one({'user_id': user_id})
            return cart
        except Exception as error:
            logger.error(f"Error retrieving cart: {error}")
            return None

    def clear_shopping_cart(self, user_id: int) -> bool:
        """
        Clear a user's shopping cart

        Args:
            user_id: User ID

        Returns:
            True if successful
        """
        try:
            collection = self._db['shopping_carts']
            collection.delete_one({'user_id': user_id})
            logger.info(f"Cart cleared for user {user_id}")
            return True
        except Exception as error:
            logger.error(f"Error clearing cart: {error}")
            return False

    def insert_user_behavior(
        self,
        user_id: int,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Log user behavior/event

        Args:
            user_id: User ID
            event_type: Type of event
            event_data: Event details

        Returns:
            Inserted document ID
        """
        try:
            collection = self._db['user_behavior']
            behavior_doc = {
                'user_id': user_id,
                'event_type': event_type,
                'event_data': event_data,
                'timestamp': datetime.utcnow()
            }
            result = collection.insert_one(behavior_doc)
            logger.info(f"Behavior logged for user {user_id}: {event_type}")
            return str(result.inserted_id)
        except Exception as error:
            logger.error(f"Error logging behavior: {error}")
            raise

    def get_user_behavior(
        self,
        user_id: int,
        event_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get user behavior history

        Args:
            user_id: User ID
            event_type: Optional event type filter
            limit: Maximum number of records to return

        Returns:
            List of behavior records
        """
        try:
            collection = self._db['user_behavior']
            query = {'user_id': user_id}
            if event_type:
                query['event_type'] = event_type

            behaviors = list(collection.find(query).sort('timestamp', -1).limit(limit))
            return behaviors
        except Exception as error:
            logger.error(f"Error retrieving behavior: {error}")
            return []

    def insert_document(
        self,
        collection_name: str,
        document: Dict[str, Any]
    ) -> Optional[str]:
        """
        Insert a generic document

        Args:
            collection_name: Collection name
            document: Document to insert

        Returns:
            Inserted document ID
        """
        try:
            collection = self._db[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as error:
            logger.error(f"Error inserting document: {error}")
            raise

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")


# Singleton instance
mongodb_client = MongoDBClient()

