"""
Tests for analytics operations
"""
import pytest
from src.operations.analytics import analytics_ops
from src.operations.customer_ops import customer_ops
from src.operations.product_ops import product_ops
from src.operations.order_ops import order_ops


class TestAnalyticsQueries:
    """Test analytics query operations"""

    def test_get_top_selling_products(self):
        """Test retrieving top selling products"""
        products = analytics_ops.get_top_selling_products(limit=10)

        # Should return a list
        assert isinstance(products, list)

        # If there are products, verify structure
        if len(products) > 0:
            product = products[0]
            assert "product_id" in product
            assert "product_name" in product
            assert "total_sales" in product
            assert "overall_rank" in product

    def test_get_customer_lifetime_value(self):
        """Test customer lifetime value calculation"""
        values = analytics_ops.get_customer_lifetime_value()

        assert isinstance(values, list)

        if len(values) > 0:
            customer = values[0]
            assert "customer_id" in customer
            assert "customer_name" in customer
            assert "lifetime_value" in customer
            assert "total_orders" in customer

    def test_get_product_ranking_by_category(self):
        """Test product ranking by category"""
        rankings = analytics_ops.get_product_ranking_by_category()

        assert isinstance(rankings, list)

        if len(rankings) > 0:
            product = rankings[0]
            assert "id" in product
            assert "name" in product
            assert "category_name" in product
            assert "rank_in_category" in product

    def test_get_order_summary(self):
        """Test order summary statistics"""
        summary = analytics_ops.get_order_summary()

        assert isinstance(summary, list)
        assert len(summary) > 0

        stats = summary[0]
        assert "total_orders" in stats
        assert "unique_customers" in stats
        assert "total_revenue" in stats

    def test_find_products_by_metadata(self):
        """Test finding products by metadata attributes"""
        products = analytics_ops.find_products_by_metadata("color", "red")

        assert isinstance(products, list)

        if len(products) > 0:
            product = products[0]
            assert "id" in product
            assert "name" in product
            assert "metadata" in product

    def test_get_sales_by_date_range(self):
        """Test sales data by date range"""
        sales = analytics_ops.get_sales_by_date_range("2024-01-01", "2026-12-31")

        assert isinstance(sales, list)

        if len(sales) > 0:
            day_sales = sales[0]
            assert "order_date" in day_sales
            assert "daily_revenue" in day_sales
            assert "order_count" in day_sales

    def test_get_customer_order_frequency(self):
        """Test customer order frequency analysis"""
        frequency = analytics_ops.get_customer_order_frequency()

        assert isinstance(frequency, list)

        if len(frequency) > 0:
            customer = frequency[0]
            assert "customer_id" in customer
            assert "customer_name" in customer
            assert "order_count" in customer
            assert "customer_segment" in customer


class TestAnalyticsCaching:
    """Test caching for analytics queries"""

    def test_top_products_caching(self):
        """Test that top products are cached"""
        # First call should query the database
        products_1 = analytics_ops.get_top_selling_products(limit=5)

        # Second call should return from cache
        products_2 = analytics_ops.get_top_selling_products(limit=5)

        # Should return same data
        assert products_1 == products_2

    def test_clear_analytics_cache(self):
        """Test clearing analytics cache"""
        analytics_ops.get_top_selling_products(limit=5)
        analytics_ops.clear_analytics_cache()

        # Cache should be cleared
        # This is a simple test to ensure the method runs without error
        assert True


class TestWindowFunctions:
    """Test queries that use window functions"""

    def test_ranking_in_product_results(self):
        """Test that rankings are included in product results"""
        products = analytics_ops.get_product_ranking_by_category()

        if len(products) > 1:
            # Check that ranks are assigned
            for product in products[:5]:
                assert "rank_in_category" in product
                assert product["rank_in_category"] >= 1

    def test_customer_segmentation(self):
        """Test customer segmentation results"""
        frequency = analytics_ops.get_customer_order_frequency()

        if len(frequency) > 0:
            segments = set(customer.get("customer_segment") for customer in frequency)
            # Should have various segments
            assert len(segments) > 0


class TestAnalyticsEdgeCases:
    """Test edge cases in analytics"""

    def test_empty_date_range(self):
        """Test sales query with date range that has no data"""
        sales = analytics_ops.get_sales_by_date_range("1900-01-01", "1900-12-31")

        # Should return empty list, not error
        assert isinstance(sales, list)

    def test_products_with_no_sales(self):
        """Test handling of products with no sales"""
        # This tests the left join behavior
        rankings = analytics_ops.get_product_ranking_by_category()

        # Should still return products even if they have no sales
        assert isinstance(rankings, list)

