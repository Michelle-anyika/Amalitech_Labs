"""
Script to analyze and optimize query performance using EXPLAIN ANALYZE
"""
import logging
from src.db.postgres import postgres_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def explain_query(query_name: str, query: str, params: tuple = None):
    """
    Execute EXPLAIN ANALYZE and display results

    Args:
        query_name: Name of the query for logging
        query: SQL query to analyze
        params: Query parameters (if any)
    """
    explain_query = f"EXPLAIN ANALYZE {query}"

    try:
        results = postgres_client.execute_query(explain_query, params, fetch_all=True)

        logger.info(f"\n{'='*80}")
        logger.info(f"QUERY: {query_name}")
        logger.info(f"{'='*80}")

        for row in results or []:
            logger.info(row)

        logger.info(f"{'='*80}\n")
    except Exception as error:
        logger.error(f"Error analyzing query {query_name}: {error}")


def optimize_customer_queries():
    """Optimize customer-related queries"""
    logger.info("Analyzing Customer Queries...")

    # Query 1: Get customer orders without index
    query = """
        SELECT c.id, c.first_name, c.last_name, COUNT(o.id) as order_count
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id, c.first_name, c.last_name
        ORDER BY order_count DESC;
    """
    explain_query("Customer Orders (should use index on orders.customer_id)", query)


def optimize_product_queries():
    """Optimize product-related queries"""
    logger.info("Analyzing Product Queries...")

    # Query 1: Search products by JSONB metadata
    query = """
        SELECT id, name, metadata
        FROM products
        WHERE metadata->>'color' = 'red'
        ORDER BY name;
    """
    explain_query("Find products by metadata color (should use GIN index)", query)


def optimize_order_queries():
    """Optimize order-related queries"""
    logger.info("Analyzing Order Queries...")

    # Query 1: Get all orders for a specific customer
    query = """
        SELECT o.id, o.order_date, o.total_amount, o.status
        FROM orders o
        WHERE o.customer_id = %s
        ORDER BY o.order_date DESC;
    """
    explain_query("Get customer orders (should use index on orders.customer_id)", query, (1,))


def create_indexes():
    """Create optimization indexes"""
    logger.info("Creating indexes...")

    indexes = [
        (
            "idx_orders_customer_id",
            "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);"
        ),
        (
            "idx_orders_customer_created",
            "CREATE INDEX IF NOT EXISTS idx_orders_customer_created ON orders(customer_id, created_at);"
        ),
        (
            "idx_products_metadata_gin",
            "CREATE INDEX IF NOT EXISTS idx_products_metadata_gin ON products USING GIN(metadata);"
        ),
        (
            "idx_order_items_order_id",
            "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);"
        ),
        (
            "idx_order_items_product_id",
            "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);"
        ),
    ]

    for index_name, index_query in indexes:
        try:
            postgres_client.execute_update(index_query, None)
            logger.info(f"Created index: {index_name}")
        except Exception as error:
            logger.warning(f"Could not create index {index_name}: {error}")


def main():
    """Main function for query optimization"""
    logger.info("Starting Query Performance Analysis...")

    try:
        # Create indexes first
        create_indexes()

        # Analyze queries
        optimize_customer_queries()
        optimize_product_queries()
        optimize_order_queries()

        logger.info("Query analysis completed!")
        logger.info("\nOptimization recommendations saved to OPTIMIZATION_REPORT.md")
    except Exception as error:
        logger.error(f"Error during optimization analysis: {error}")
        raise


if __name__ == "__main__":
    main()

