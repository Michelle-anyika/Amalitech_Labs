"""
Tests for MongoDB operations
"""
import pytest
from datetime import datetime
from src.db.mongodb_client import mongodb_client


class TestMongoDBSessions:
    """Test MongoDB session operations"""

    def test_insert_and_get_session(self):
        """Test inserting and retrieving a session"""
        user_id = 1
        session_data = {
            "session_id": "test_session_123",
            "login_time": datetime.utcnow().isoformat(),
            "pages_visited": ["home", "products", "cart"]
        }

        doc_id = mongodb_client.insert_session(user_id, session_data)
        assert doc_id is not None

        retrieved = mongodb_client.get_session(user_id)
        assert retrieved is not None
        assert retrieved["user_id"] == user_id
        assert retrieved["data"]["session_id"] == "test_session_123"

    def test_session_update(self):
        """Test updating a session"""
        user_id = 2
        initial_data = {"pages": ["home"]}
        updated_data = {"pages": ["home", "products", "cart"]}

        mongodb_client.insert_session(user_id, initial_data)
        mongodb_client.insert_session(user_id, updated_data)

        retrieved = mongodb_client.get_session(user_id)
        assert retrieved["data"]["pages"] == ["home", "products", "cart"]


class TestMongoDBShoppingCart:
    """Test MongoDB shopping cart operations"""

    def test_insert_and_get_cart(self):
        """Test shopping cart operations"""
        user_id = 1
        cart_items = [
            {"product_id": 1, "name": "Product 1", "quantity": 2, "price": 29.99},
            {"product_id": 2, "name": "Product 2", "quantity": 1, "price": 49.99}
        ]

        doc_id = mongodb_client.insert_shopping_cart(user_id, cart_items)
        assert doc_id is not None

        retrieved = mongodb_client.get_shopping_cart(user_id)
        assert retrieved is not None
        assert len(retrieved["items"]) == 2
        assert retrieved["total_items"] == 2

    def test_clear_cart(self):
        """Test clearing a shopping cart"""
        user_id = 2
        cart_items = [{"product_id": 1, "quantity": 1, "price": 29.99}]

        mongodb_client.insert_shopping_cart(user_id, cart_items)
        assert mongodb_client.get_shopping_cart(user_id) is not None

        mongodb_client.clear_shopping_cart(user_id)
        assert mongodb_client.get_shopping_cart(user_id) is None


class TestMongoDBUserBehavior:
    """Test MongoDB user behavior tracking"""

    def test_insert_behavior(self):
        """Test inserting user behavior"""
        user_id = 1
        event_type = "view"
        event_data = {"product_id": 123, "timestamp": datetime.utcnow().isoformat()}

        doc_id = mongodb_client.insert_user_behavior(user_id, event_type, event_data)
        assert doc_id is not None

    def test_get_user_behavior(self):
        """Test retrieving user behavior"""
        user_id = 2

        # Insert multiple events
        mongodb_client.insert_user_behavior(user_id, "view", {"product_id": 1})
        mongodb_client.insert_user_behavior(user_id, "add_to_cart", {"product_id": 1})
        mongodb_client.insert_user_behavior(user_id, "view", {"product_id": 2})

        # Get all behavior
        all_behavior = mongodb_client.get_user_behavior(user_id, limit=5)
        assert len(all_behavior) >= 3

        # Get specific event type
        view_events = mongodb_client.get_user_behavior(user_id, event_type="view", limit=5)
        assert all(event["event_type"] == "view" for event in view_events)

    def test_behavior_with_limit(self):
        """Test limiting behavior results"""
        user_id = 3

        # Insert 10 events
        for i in range(10):
            mongodb_client.insert_user_behavior(
                user_id,
                "view",
                {"product_id": i, "index": i}
            )

        # Get limited results
        recent = mongodb_client.get_user_behavior(user_id, limit=3)
        assert len(recent) == 3


class TestMongoDBDocuments:
    """Test generic MongoDB document operations"""

    def test_insert_document(self):
        """Test inserting a generic document"""
        doc = {
            "user_id": 1,
            "type": "feedback",
            "rating": 5,
            "comment": "Great product!"
        }

        doc_id = mongodb_client.insert_document("feedback", doc)
        assert doc_id is not None

    def test_insert_complex_document(self):
        """Test inserting complex nested documents"""
        doc = {
            "user_id": 2,
            "type": "review",
            "product": {
                "id": 123,
                "name": "Test Product",
                "category": "Electronics"
            },
            "rating": 4,
            "pros": ["Good quality", "Fast shipping"],
            "cons": ["Packaging could be better"],
            "timestamp": datetime.utcnow().isoformat()
        }

        doc_id = mongodb_client.insert_document("reviews", doc)
        assert doc_id is not None

