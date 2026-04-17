"""
Pytest configuration and fixtures
"""
import pytest
import logging
from src.db.postgres import postgres_client
from src.db.redis_client import redis_client
from src.db.mongodb_client import mongodb_client

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session")
def db_connection():
    """Provide database connection for tests"""
    try:
        yield postgres_client
    finally:
        pass  # Keep connection open for test session


@pytest.fixture(scope="session")
def redis_connection():
    """Provide Redis connection for tests"""
    try:
        yield redis_client
    finally:
        redis_client.flush_all()  # Clean up after tests


@pytest.fixture(scope="session")
def mongodb_connection():
    """Provide MongoDB connection for tests"""
    try:
        yield mongodb_client
    finally:
        pass  # Cleanup if needed


@pytest.fixture
def cleanup_redis(redis_connection):
    """Clean Redis cache before each test"""
    redis_connection.flush_all()
    yield
    redis_connection.flush_all()


@pytest.fixture
def sample_customer_data():
    """Provide sample customer data for tests"""
    return {
        "first_name": "Test",
        "last_name": "Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "address": "123 Test St",
        "city": "Test City",
        "country": "Test Country"
    }


@pytest.fixture
def sample_product_data():
    """Provide sample product data for tests"""
    return {
        "name": "Test Product",
        "category_id": 1,
        "price": 29.99,
        "stock_quantity": 100,
        "description": "Test product description",
        "metadata": {"color": "red", "size": "large"}
    }


@pytest.fixture
def sample_order_data():
    """Provide sample order data for tests"""
    return {
        "customer_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2, "unit_price": 29.99},
            {"product_id": 2, "quantity": 1, "unit_price": 49.99}
        ]
    }

