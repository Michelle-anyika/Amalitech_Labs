"""
Complex analytical queries with window functions and CTEs
"""
import json
import logging
from typing import List, Dict, Any

from src.db.postgres import postgres_client
from src.db.redis_client import redis_client

logger = logging.getLogger(__name__)


class AnalyticsOperations:
    """Complex SQL queries for business analytics"""

    @staticmethod
    def get_top_selling_products(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top selling products using window functions
        Ranks products by total sales volume within each category

        Args:
            limit: Number of products to return

        Returns:
            List of top products with sales data
        """
        # Check cache first
        cache_key = "top_selling_products"
        cached = redis_client.get(cache_key)
        if cached:
            logger.info("Returning top products from cache")
            return cached

        query = """
            WITH product_sales AS (
                SELECT 
                    p.id,
                    p.name,
                    p.category_id,
                    SUM(oi.quantity) as total_sales,
                    SUM(oi.subtotal) as total_revenue,
                    RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as category_rank,
                    ROW_NUMBER() OVER (ORDER BY SUM(oi.quantity) DESC) as overall_rank
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                LEFT JOIN orders o ON oi.order_id = o.id
                WHERE o.status != 'cancelled' OR o.id IS NULL
                GROUP BY p.id, p.name, p.category_id
            )
            SELECT 
                id as product_id,
                name as product_name,
                category_id,
                total_sales,
                total_revenue,
                category_rank,
                overall_rank
            FROM product_sales
            WHERE total_sales > 0
            ORDER BY overall_rank
            LIMIT %s;
        """

        try:
            results = postgres_client.execute_query(query, (limit,), fetch_all=True)

            # Convert to list of dicts
            products = [dict(row) for row in results] if results else []

            # Cache for 1 hour (3600 seconds)
            redis_client.set(cache_key, products, expire_seconds=3600)

            logger.info(f"Retrieved {len(products)} top selling products")
            return products
        except Exception as error:
            logger.error(f"Error getting top selling products: {error}")
            raise

    @staticmethod
    def get_customer_lifetime_value() -> List[Dict[str, Any]]:
        """
        Calculate customer lifetime value using CTEs
        Shows total revenue per customer

        Returns:
            List of customers with their lifetime values
        """
        query = """
            WITH customer_orders AS (
                SELECT 
                    c.id,
                    c.first_name,
                    c.last_name,
                    COUNT(o.id) as total_orders,
                    SUM(o.total_amount) as lifetime_value,
                    AVG(o.total_amount) as avg_order_value,
                    MAX(o.order_date) as last_order_date,
                    MIN(o.order_date) as first_order_date
                FROM customers c
                LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
                GROUP BY c.id, c.first_name, c.last_name
            )
            SELECT 
                id as customer_id,
                CONCAT(first_name, ' ', last_name) as customer_name,
                total_orders,
                COALESCE(lifetime_value, 0) as lifetime_value,
                COALESCE(avg_order_value, 0) as avg_order_value,
                last_order_date,
                first_order_date
            FROM customer_orders
            ORDER BY lifetime_value DESC NULLS LAST;
        """

        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            return [dict(row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error calculating customer lifetime value: {error}")
            raise

    @staticmethod
    def get_product_ranking_by_category() -> List[Dict[str, Any]]:
        """
        Rank products by sales within each category using window functions

        Returns:
            Products with their category rank
        """
        query = """
            SELECT 
                p.id,
                p.name,
                c.name as category_name,
                COALESCE(SUM(oi.quantity), 0) as total_sales,
                COALESCE(SUM(oi.subtotal), 0) as total_revenue,
                RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as rank_in_category,
                DENSE_RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as dense_rank_in_category,
                ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.quantity) DESC) as row_num_in_category
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN order_items oi ON p.id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
            GROUP BY p.id, p.name, c.name, p.category_id
            ORDER BY c.name, rank_in_category;
        """

        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            return [dict(row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error getting product ranking: {error}")
            raise

    @staticmethod
    def get_order_summary() -> List[Dict[str, Any]]:
        """Get summary statistics about orders"""
        query = """
            SELECT 
                COUNT(DISTINCT o.id) as total_orders,
                COUNT(DISTINCT o.customer_id) as unique_customers,
                SUM(o.total_amount) as total_revenue,
                AVG(o.total_amount) as avg_order_value,
                MIN(o.total_amount) as min_order_value,
                MAX(o.total_amount) as max_order_value,
                SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) as delivered_orders,
                SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) as pending_orders,
                SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_orders
            FROM orders o;
        """

        try:
            result = postgres_client.execute_query(query, fetch_one=True)
            return [dict(result)] if result else []
        except Exception as error:
            logger.error(f"Error getting order summary: {error}")
            raise

    @staticmethod
    def find_products_by_metadata(attribute: str, value: str) -> List[Dict[str, Any]]:
        """
        Find products with specific metadata attributes using GIN index

        Args:
            attribute: Metadata key (e.g., 'color')
            value: Metadata value (e.g., 'red')

        Returns:
            List of matching products
        """
        query = """
            SELECT 
                id,
                name,
                price,
                stock_quantity,
                metadata
            FROM products
            WHERE metadata ->> %s = %s
            ORDER BY name;
        """

        try:
            results = postgres_client.execute_query(query, (attribute, value), fetch_all=True)
            return [dict(row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error finding products by metadata: {error}")
            raise

    @staticmethod
    def get_sales_by_date_range(start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get sales data within a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Sales data grouped by date
        """
        query = """
            SELECT 
                DATE(o.order_date) as order_date,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as daily_revenue,
                AVG(o.total_amount) as avg_order_value,
                COUNT(DISTINCT o.customer_id) as unique_customers
            FROM orders o
            WHERE o.order_date::DATE BETWEEN %s::DATE AND %s::DATE
              AND o.status != 'cancelled'
            GROUP BY DATE(o.order_date)
            ORDER BY order_date DESC;
        """

        try:
            results = postgres_client.execute_query(query, (start_date, end_date), fetch_all=True)
            return [dict(row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error getting sales by date range: {error}")
            raise

    @staticmethod
    def get_customer_order_frequency() -> List[Dict[str, Any]]:
        """
        Analyze customer order frequency and segments
        """
        query = """
            WITH customer_stats AS (
                SELECT 
                    c.id,
                    c.first_name,
                    c.last_name,
                    COUNT(o.id) as order_count,
                    SUM(o.total_amount) as total_spent,
                    CASE 
                        WHEN COUNT(o.id) = 0 THEN 'No Orders'
                        WHEN COUNT(o.id) = 1 THEN 'Single Order'
                        WHEN COUNT(o.id) BETWEEN 2 AND 5 THEN 'Regular'
                        ELSE 'Frequent'
                    END as customer_segment
                FROM customers c
                LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled'
                GROUP BY c.id, c.first_name, c.last_name
            )
            SELECT 
                id as customer_id,
                CONCAT(first_name, ' ', last_name) as customer_name,
                order_count,
                COALESCE(total_spent, 0) as total_spent,
                customer_segment
            FROM customer_stats
            ORDER BY order_count DESC, total_spent DESC;
        """

        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            return [dict(row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error analyzing customer frequency: {error}")
            raise

    @staticmethod
    def clear_analytics_cache():
        """Clear analytics cache"""
        redis_client.delete("top_selling_products")
        logger.info("Analytics cache cleared")


# Singleton instance
analytics_ops = AnalyticsOperations()

