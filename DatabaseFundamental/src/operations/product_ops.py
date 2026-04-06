"""
Product CRUD operations with JSONB metadata support
"""
import json
import logging
from typing import List, Dict, Any, Optional

from src.db.postgres import postgres_client
from src.db.redis_client import redis_client
from src.models.schemas import Product

logger = logging.getLogger(__name__)


class ProductOperations:
    """Handle all product-related database operations"""

    @staticmethod
    def create_product(
        name: str,
        category_id: int,
        price: float,
        stock_quantity: int,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Create a new product with JSONB metadata

        Args:
            name: Product name
            category_id: Category ID
            price: Product price
            stock_quantity: Stock quantity
            description: Product description
            metadata: JSONB metadata (sizes, colors, etc.)

        Returns:
            Product ID
        """
        metadata_json = json.dumps(metadata) if metadata else '{}'

        query = """
            INSERT INTO products (name, category_id, price, stock_quantity, description, metadata)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb)
            RETURNING id;
        """
        params = (name, category_id, price, stock_quantity, description, metadata_json)

        try:
            result = postgres_client.execute_query(query, params, fetch_one=True)
            product_id = result['id']
            logger.info(f"Product created with ID: {product_id}")
            return product_id
        except Exception as error:
            logger.error(f"Error creating product: {error}")
            raise

    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        query = """
            SELECT id, name, category_id, price, stock_quantity, description,
                   metadata, created_at, updated_at
            FROM products
            WHERE id = %s;
        """
        try:
            result = postgres_client.execute_query(query, (product_id,), fetch_one=True)
            if result:
                result['metadata'] = result.get('metadata') or {}
                return Product(**result)
            return None
        except Exception as error:
            logger.error(f"Error getting product: {error}")
            raise

    @staticmethod
    def get_all_products() -> List[Product]:
        """Get all products"""
        query = """
            SELECT id, name, category_id, price, stock_quantity, description,
                   metadata, created_at, updated_at
            FROM products
            ORDER BY created_at DESC;
        """
        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            products = []
            for row in results or []:
                row['metadata'] = row.get('metadata') or {}
                products.append(Product(**row))
            return products
        except Exception as error:
            logger.error(f"Error getting all products: {error}")
            raise

    @staticmethod
    def get_products_by_category(category_id: int) -> List[Product]:
        """Get products by category"""
        query = """
            SELECT id, name, category_id, price, stock_quantity, description,
                   metadata, created_at, updated_at
            FROM products
            WHERE category_id = %s
            ORDER BY name;
        """
        try:
            results = postgres_client.execute_query(query, (category_id,), fetch_all=True)
            products = []
            for row in results or []:
                row['metadata'] = row.get('metadata') or {}
                products.append(Product(**row))
            return products
        except Exception as error:
            logger.error(f"Error getting products by category: {error}")
            raise

    @staticmethod
    def update_product(
        product_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        stock_quantity: Optional[int] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update a product"""
        updates = []
        params = []

        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if price is not None:
            updates.append("price = %s")
            params.append(price)
        if stock_quantity is not None:
            updates.append("stock_quantity = %s")
            params.append(stock_quantity)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if metadata is not None:
            updates.append("metadata = %s::jsonb")
            params.append(json.dumps(metadata))

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(product_id)

        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s;"

        try:
            postgres_client.execute_update(query, tuple(params))
            # Invalidate cache when product is updated
            redis_client.delete(f"product:{product_id}")
            logger.info(f"Product {product_id} updated")
            return True
        except Exception as error:
            logger.error(f"Error updating product: {error}")
            raise

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """Delete a product"""
        query = "DELETE FROM products WHERE id = %s;"

        try:
            postgres_client.execute_update(query, (product_id,))
            redis_client.delete(f"product:{product_id}")
            logger.info(f"Product {product_id} deleted")
            return True
        except Exception as error:
            logger.error(f"Error deleting product: {error}")
            raise

    @staticmethod
    def search_products_by_metadata(attribute_key: str, attribute_value: Any) -> List[Product]:
        """
        Search products by JSONB metadata attribute using GIN index

        Args:
            attribute_key: Metadata key to search
            attribute_value: Value to match

        Returns:
            List of matching products
        """
        query = f"""
            SELECT id, name, category_id, price, stock_quantity, description,
                   metadata, created_at, updated_at
            FROM products
            WHERE metadata->%s = to_jsonb(%s)
            ORDER BY name;
        """
        try:
            results = postgres_client.execute_query(
                query,
                (attribute_key, json.dumps(attribute_value)),
                fetch_all=True
            )
            products = []
            for row in results or []:
                row['metadata'] = row.get('metadata') or {}
                products.append(Product(**row))
            return products
        except Exception as error:
            logger.error(f"Error searching by metadata: {error}")
            raise

    @staticmethod
    def get_products_in_stock() -> List[Product]:
        """Get all products with stock > 0"""
        query = """
            SELECT id, name, category_id, price, stock_quantity, description,
                   metadata, created_at, updated_at
            FROM products
            WHERE stock_quantity > 0
            ORDER BY stock_quantity DESC;
        """
        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            products = []
            for row in results or []:
                row['metadata'] = row.get('metadata') or {}
                products.append(Product(**row))
            return products
        except Exception as error:
            logger.error(f"Error getting products in stock: {error}")
            raise


# Singleton instance
product_ops = ProductOperations()

