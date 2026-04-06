"""
Tests for PostgreSQL operations
"""
import pytest
from src.operations.customer_ops import customer_ops
from src.operations.product_ops import product_ops
from src.operations.order_ops import order_ops
from src.models.schemas import OrderStatus


class TestCustomerOperations:
    """Test customer CRUD operations"""

    def test_create_customer(self, sample_customer_data):
        """Test creating a customer"""
        customer_id = customer_ops.create_customer(**sample_customer_data)
        assert customer_id is not None
        assert isinstance(customer_id, int)

    def test_get_customer(self, sample_customer_data):
        """Test retrieving a customer"""
        customer_id = customer_ops.create_customer(**sample_customer_data)
        customer = customer_ops.get_customer(customer_id)

        assert customer is not None
        assert customer.first_name == sample_customer_data["first_name"]
        assert customer.email == sample_customer_data["email"]

    def test_update_customer(self, sample_customer_data):
        """Test updating a customer"""
        customer_id = customer_ops.create_customer(**sample_customer_data)
        updated = customer_ops.update_customer(customer_id, first_name="Updated")

        assert updated is True
        customer = customer_ops.get_customer(customer_id)
        assert customer.first_name == "Updated"

    def test_get_customer_by_email(self, sample_customer_data):
        """Test retrieving customer by email"""
        customer_ops.create_customer(**sample_customer_data)
        customer = customer_ops.get_customer_by_email(sample_customer_data["email"])

        assert customer is not None
        assert customer.email == sample_customer_data["email"]


class TestProductOperations:
    """Test product CRUD operations"""

    def test_create_product(self, sample_product_data):
        """Test creating a product"""
        product_id = product_ops.create_product(**sample_product_data)
        assert product_id is not None
        assert isinstance(product_id, int)

    def test_get_product(self, sample_product_data):
        """Test retrieving a product"""
        product_id = product_ops.create_product(**sample_product_data)
        product = product_ops.get_product(product_id)

        assert product is not None
        assert product.name == sample_product_data["name"]
        assert product.price == sample_product_data["price"]

    def test_update_product(self, sample_product_data):
        """Test updating a product"""
        product_id = product_ops.create_product(**sample_product_data)
        updated = product_ops.update_product(product_id, price=39.99)

        assert updated is True
        product = product_ops.get_product(product_id)
        assert product.price == 39.99

    def test_search_products_by_metadata(self, sample_product_data):
        """Test searching products by metadata"""
        product_ops.create_product(**sample_product_data)
        products = product_ops.search_products_by_metadata("color", "red")

        assert len(products) > 0


class TestOrderOperations:
    """Test order operations"""

    def test_create_order(self, sample_customer_data, sample_product_data, sample_order_data):
        """Test creating an order"""
        # Create customer and product first
        customer_id = customer_ops.create_customer(**sample_customer_data)
        product_id = product_ops.create_product(**sample_product_data)

        # Update order data with real IDs
        sample_order_data["customer_id"] = customer_id
        sample_order_data["items"][0]["product_id"] = product_id

        order_id = order_ops.create_order(
            sample_order_data["customer_id"],
            sample_order_data["items"]
        )

        assert order_id is not None
        assert isinstance(order_id, int)

    def test_get_order(self, sample_customer_data, sample_product_data, sample_order_data):
        """Test retrieving an order"""
        # Create customer, product, and order
        customer_id = customer_ops.create_customer(**sample_customer_data)
        product_id = product_ops.create_product(**sample_product_data)

        sample_order_data["customer_id"] = customer_id
        sample_order_data["items"][0]["product_id"] = product_id

        order_id = order_ops.create_order(
            sample_order_data["customer_id"],
            sample_order_data["items"]
        )

        order = order_ops.get_order(order_id)
        assert order is not None
        assert order.customer_id == customer_id

    def test_update_order_status(self, sample_customer_data, sample_product_data, sample_order_data):
        """Test updating order status"""
        # Setup
        customer_id = customer_ops.create_customer(**sample_customer_data)
        product_id = product_ops.create_product(**sample_product_data)

        sample_order_data["customer_id"] = customer_id
        sample_order_data["items"][0]["product_id"] = product_id

        order_id = order_ops.create_order(
            sample_order_data["customer_id"],
            sample_order_data["items"]
        )

        # Update status
        updated = order_ops.update_order_status(order_id, OrderStatus.SHIPPED, "Shipped via FedEx")
        assert updated is True


class TestTransactionalIntegrity:
    """Test ACID properties of transactions"""

    def test_order_creation_is_atomic(self, sample_customer_data, sample_product_data):
        """Test that order creation is atomic"""
        customer_id = customer_ops.create_customer(**sample_customer_data)
        product_id = product_ops.create_product(**sample_product_data)

        items = [
            {"product_id": product_id, "quantity": 2, "unit_price": sample_product_data["price"]}
        ]

        initial_stock = sample_product_data["stock_quantity"]

        order_id = order_ops.create_order(customer_id, items)

        # Verify stock was updated
        updated_product = product_ops.get_product(product_id)
        assert updated_product.stock_quantity == initial_stock - 2

        # Verify order was created
        order = order_ops.get_order(order_id)
        assert order is not None

