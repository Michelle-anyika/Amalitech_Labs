"""
Script to populate database with sample data
"""
import logging
from datetime import datetime, timedelta
from src.db.postgres import postgres_client
from src.operations.customer_ops import customer_ops
from src.operations.product_ops import product_ops
from src.operations.order_ops import order_ops
from src.db.mongodb_client import mongodb_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_categories():
    """Create sample product categories"""
    categories = [
        ("Electronics", "Electronic devices and gadgets"),
        ("Clothing", "Apparel and accessories"),
        ("Books", "Physical and digital books"),
        ("Home & Garden", "Home and garden products"),
        ("Sports", "Sports and outdoor equipment"),
    ]

    query = """
        INSERT INTO categories (name, description)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """

    for name, description in categories:
        postgres_client.execute_update(query, (name, description))

    logger.info(f"Created {len(categories)} categories")


def create_customers():
    """Create sample customers"""
    customers_data = [
        ("John", "Doe", "john.doe@example.com", "+1234567890", "123 Main St", "New York", "USA"),
        ("Jane", "Smith", "jane.smith@example.com", "+0987654321", "456 Oak Ave", "Los Angeles", "USA"),
        ("Bob", "Johnson", "bob.johnson@example.com", "+1122334455", "789 Pine Rd", "Chicago", "USA"),
        ("Alice", "Williams", "alice.williams@example.com", "+5566778899", "321 Elm St", "Houston", "USA"),
        ("Charlie", "Brown", "charlie.brown@example.com", "+9988776655", "654 Maple Dr", "Phoenix", "USA"),
    ]

    customer_ids = []
    for first, last, email, phone, address, city, country in customers_data:
        try:
            cid = customer_ops.create_customer(first, last, email, phone, address, city, country)
            customer_ids.append(cid)
        except Exception as e:
            logger.warning(f"Customer might already exist: {e}")

    logger.info(f"Created {len(customer_ids)} customers")
    return customer_ids


def create_products():
    """Create sample products with metadata"""
    products_data = [
        (
            "Laptop Pro",
            1,
            999.99,
            50,
            "High-performance laptop",
            {"brand": "TechBrand", "processor": "Intel i7", "ram": "16GB", "colors": ["silver", "black"]}
        ),
        (
            "Wireless Earbuds",
            1,
            79.99,
            100,
            "Premium wireless earbuds",
            {"brand": "AudioPro", "battery": "8 hours", "colors": ["black", "white", "blue"]}
        ),
        (
            "Cotton T-Shirt",
            2,
            29.99,
            200,
            "Comfortable cotton t-shirt",
            {"material": "100% cotton", "sizes": ["S", "M", "L", "XL"], "colors": ["red", "blue", "green"]}
        ),
        (
            "Denim Jeans",
            2,
            59.99,
            150,
            "Classic blue denim jeans",
            {"material": "Denim", "sizes": ["28", "30", "32", "34", "36"], "colors": ["blue", "black"]}
        ),
        (
            "Python Programming",
            3,
            39.99,
            75,
            "Learn Python programming basics",
            {"author": "Expert Developer", "pages": 500, "format": ["hardcover", "ebook"]}
        ),
        (
            "Garden Tool Set",
            4,
            45.99,
            60,
            "Complete garden tool set",
            {"tools": ["shovel", "rake", "hoe", "spade"], "material": "stainless steel"}
        ),
        (
            "Running Shoes",
            5,
            89.99,
            100,
            "Professional running shoes",
            {"brand": "SportBrand", "sizes": ["6", "7", "8", "9", "10", "11", "12"], "colors": ["black", "white", "red"]}
        ),
    ]

    product_ids = []
    for name, cat_id, price, stock, desc, metadata in products_data:
        try:
            pid = product_ops.create_product(name, cat_id, price, stock, desc, metadata)
            product_ids.append(pid)
        except Exception as e:
            logger.warning(f"Product might already exist: {e}")

    logger.info(f"Created {len(product_ids)} products")
    return product_ids


def create_sample_orders(customer_ids, product_ids):
    """Create sample orders"""
    if not customer_ids or not product_ids:
        logger.warning("No customers or products available")
        return

    orders_created = 0

    for i, customer_id in enumerate(customer_ids):
        # Create 2-4 orders per customer
        num_orders = (i % 3) + 2

        for order_num in range(num_orders):
            try:
                # Pick random products (1-3 items per order)
                num_items = (order_num % 3) + 1
                items = []

                for j in range(num_items):
                    product_id = product_ids[(order_num * 2 + j) % len(product_ids)]

                    # Get product price
                    product = product_ops.get_product(product_id)
                    if product:
                        items.append({
                            "product_id": product_id,
                            "quantity": (j % 3) + 1,
                            "unit_price": product.price
                        })

                if items:
                    order_ops.create_order(customer_id, items)
                    orders_created += 1
            except Exception as e:
                logger.warning(f"Error creating order: {e}")

    logger.info(f"Created {orders_created} orders")


def populate_mongodb():
    """Populate MongoDB with sample session and behavior data"""
    try:
        # Sample sessions
        for user_id in range(1, 6):
            session_data = {
                "session_id": f"sess_{user_id}_{datetime.now().timestamp()}",
                "login_time": datetime.utcnow().isoformat(),
                "pages_visited": ["home", "products", "cart"],
                "last_activity": datetime.utcnow().isoformat()
            }
            mongodb_client.insert_session(user_id, session_data)

        # Sample shopping carts
        for user_id in range(1, 6):
            cart_items = [
                {"product_id": user_id, "name": f"Product {user_id}", "quantity": 1, "price": 29.99},
                {"product_id": user_id + 1, "name": f"Product {user_id + 1}", "quantity": 2, "price": 49.99}
            ]
            mongodb_client.insert_shopping_cart(user_id, cart_items)

        # Sample behavior events
        event_types = ["view", "add_to_cart", "remove_from_cart", "checkout"]
        for user_id in range(1, 6):
            for event_type in event_types:
                event_data = {
                    "product_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
                mongodb_client.insert_user_behavior(user_id, event_type, event_data)

        logger.info("MongoDB sample data populated")
    except Exception as e:
        logger.error(f"Error populating MongoDB: {e}")


def main():
    """Main function to populate database"""
    logger.info("Starting database population...")

    try:
        create_categories()
        customer_ids = create_customers()
        product_ids = create_products()
        create_sample_orders(customer_ids, product_ids)
        populate_mongodb()

        logger.info("Database population completed successfully!")
    except Exception as error:
        logger.error(f"Error during population: {error}")
        raise


if __name__ == "__main__":
    main()

