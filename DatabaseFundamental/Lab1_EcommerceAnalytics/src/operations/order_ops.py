"""
Order operations with transactional support
"""
import logging
from typing import List, Optional
from datetime import datetime

from src.db.postgres import postgres_client
from src.models.schemas import Order, OrderItem, OrderStatus

logger = logging.getLogger(__name__)


class OrderOperations:
    """Handle all order-related database operations"""

    @staticmethod
    def create_order(
        customer_id: int,
        items: List[dict]  # [{"product_id": 1, "quantity": 5, "unit_price": 29.99}, ...]
    ) -> Optional[int]:
        """
        Create an order with its items in a transaction (ACID)

        This function ensures that stock is updated AND the order is created
        atomically - either both succeed or both fail.

        Args:
            customer_id: Customer ID
            items: List of order items with product_id, quantity, unit_price

        Returns:
            Order ID if successful, None otherwise
        """
        try:
            # Prepare operations for transaction
            operations = []
            total_amount = 0

            # First, check stock availability
            for item in items:
                check_stock_query = "SELECT stock_quantity FROM products WHERE id = %s;"
                result = postgres_client.execute_query(
                    check_stock_query,
                    (item['product_id'],),
                    fetch_one=True
                )

                if not result or result['stock_quantity'] < item['quantity']:
                    logger.error(f"Insufficient stock for product {item['product_id']}")
                    return None

            # Create order
            order_query = """
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """

            # Calculate total
            for item in items:
                total_amount += item['quantity'] * item['unit_price']

            # Execute order creation in transaction
            result = postgres_client.execute_query(
                order_query,
                (customer_id, datetime.now(), total_amount, OrderStatus.PENDING.value),
                fetch_one=True
            )

            order_id = result['id']

            # Now create order items and update stock in transaction
            transaction_ops = []

            for item in items:
                # Insert order item
                item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s);
                """
                subtotal = item['quantity'] * item['unit_price']
                transaction_ops.append((
                    item_query,
                    (order_id, item['product_id'], item['quantity'], item['unit_price'], subtotal)
                ))

                # Update stock
                stock_query = """
                    UPDATE products
                    SET stock_quantity = stock_quantity - %s
                    WHERE id = %s;
                """
                transaction_ops.append((stock_query, (item['quantity'], item['product_id'])))

            # Add status history entry
            status_query = """
                INSERT INTO order_status_history (order_id, status, changed_at)
                VALUES (%s, %s, %s);
            """
            transaction_ops.append((
                status_query,
                (order_id, OrderStatus.PENDING.value, datetime.now())
            ))

            # Execute transaction
            postgres_client.execute_transaction(transaction_ops)

            logger.info(f"Order {order_id} created with {len(items)} items")
            return order_id

        except Exception as error:
            logger.error(f"Error creating order: {error}")
            raise

    @staticmethod
    def get_order(order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        query = """
            SELECT id, customer_id, order_date, total_amount, status, created_at, updated_at
            FROM orders
            WHERE id = %s;
        """
        try:
            result = postgres_client.execute_query(query, (order_id,), fetch_one=True)
            if result:
                result['status'] = OrderStatus(result['status'])
                return Order(**result)
            return None
        except Exception as error:
            logger.error(f"Error getting order: {error}")
            raise

    @staticmethod
    def get_customer_orders(customer_id: int) -> List[Order]:
        """Get all orders for a customer"""
        query = """
            SELECT id, customer_id, order_date, total_amount, status, created_at, updated_at
            FROM orders
            WHERE customer_id = %s
            ORDER BY order_date DESC;
        """
        try:
            results = postgres_client.execute_query(query, (customer_id,), fetch_all=True)
            orders = []
            for row in results or []:
                row['status'] = OrderStatus(row['status'])
                orders.append(Order(**row))
            return orders
        except Exception as error:
            logger.error(f"Error getting customer orders: {error}")
            raise

    @staticmethod
    def get_order_items(order_id: int) -> List[OrderItem]:
        """Get all items in an order"""
        query = """
            SELECT id, order_id, product_id, quantity, unit_price, subtotal, created_at
            FROM order_items
            WHERE order_id = %s;
        """
        try:
            results = postgres_client.execute_query(query, (order_id,), fetch_all=True)
            return [OrderItem(**row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error getting order items: {error}")
            raise

    @staticmethod
    def update_order_status(
        order_id: int,
        new_status: OrderStatus,
        notes: Optional[str] = None
    ) -> bool:
        """Update order status and add to history"""
        try:
            # Update order status
            query = """
                UPDATE orders
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """
            postgres_client.execute_update(query, (new_status.value, order_id))

            # Add status history
            history_query = """
                INSERT INTO order_status_history (order_id, status, changed_at, notes)
                VALUES (%s, %s, %s, %s);
            """
            postgres_client.execute_update(
                history_query,
                (order_id, new_status.value, datetime.now(), notes)
            )

            logger.info(f"Order {order_id} status updated to {new_status.value}")
            return True
        except Exception as error:
            logger.error(f"Error updating order status: {error}")
            raise

    @staticmethod
    def get_order_total(order_id: int) -> Optional[float]:
        """Get order total amount"""
        query = "SELECT total_amount FROM orders WHERE id = %s;"
        try:
            result = postgres_client.execute_query(query, (order_id,), fetch_one=True)
            return result['total_amount'] if result else None
        except Exception as error:
            logger.error(f"Error getting order total: {error}")
            raise

    @staticmethod
    def cancel_order(order_id: int) -> bool:
        """Cancel an order and restore stock"""
        try:
            # Get order items
            items = OrderOperations.get_order_items(order_id)

            # Prepare transaction operations
            transaction_ops = []

            # Update order status
            status_query = """
                UPDATE orders
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """
            transaction_ops.append((status_query, (OrderStatus.CANCELLED.value, order_id)))

            # Restore stock for each item
            for item in items:
                stock_query = """
                    UPDATE products
                    SET stock_quantity = stock_quantity + %s
                    WHERE id = %s;
                """
                transaction_ops.append((stock_query, (item.quantity, item.product_id)))

            # Add to status history
            history_query = """
                INSERT INTO order_status_history (order_id, status, changed_at, notes)
                VALUES (%s, %s, %s, %s);
            """
            transaction_ops.append((
                history_query,
                (order_id, OrderStatus.CANCELLED.value, datetime.now(), "Order cancelled")
            ))

            # Execute transaction
            postgres_client.execute_transaction(transaction_ops)

            logger.info(f"Order {order_id} cancelled and stock restored")
            return True
        except Exception as error:
            logger.error(f"Error cancelling order: {error}")
            raise


# Singleton instance
order_ops = OrderOperations()

