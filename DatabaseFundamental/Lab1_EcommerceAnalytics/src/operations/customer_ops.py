"""
Customer CRUD operations
"""
import logging
from typing import List, Optional

from src.db.postgres import postgres_client
from src.models.schemas import Customer

logger = logging.getLogger(__name__)


class CustomerOperations:
    """Handle all customer-related database operations"""
    
    @staticmethod
    def create_customer(
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None
    ) -> int:
        """
        Create a new customer
        
        Args:
            first_name: Customer first name
            last_name: Customer last name
            email: Customer email
            phone: Customer phone number
            address: Customer address
            city: Customer city
            country: Customer country
        
        Returns:
            Customer ID
        """
        query = """
            INSERT INTO customers (first_name, last_name, email, phone, address, city, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        params = (first_name, last_name, email, phone, address, city, country)
        
        try:
            result = postgres_client.execute_query(query, params, fetch_one=True)
            customer_id = result['id']
            logger.info(f"Customer created with ID: {customer_id}")
            return customer_id
        except Exception as error:
            logger.error(f"Error creating customer: {error}")
            raise
    
    @staticmethod
    def get_customer(customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        query = """
            SELECT id, first_name, last_name, email, phone, address, city, country,
                   created_at, updated_at
            FROM customers
            WHERE id = %s;
        """
        try:
            result = postgres_client.execute_query(query, (customer_id,), fetch_one=True)
            if result:
                return Customer(**result)
            return None
        except Exception as error:
            logger.error(f"Error getting customer: {error}")
            raise
    
    @staticmethod
    def get_all_customers() -> List[Customer]:
        """Get all customers"""
        query = """
            SELECT id, first_name, last_name, email, phone, address, city, country,
                   created_at, updated_at
            FROM customers
            ORDER BY created_at DESC;
        """
        try:
            results = postgres_client.execute_query(query, fetch_all=True)
            return [Customer(**row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error getting all customers: {error}")
            raise
    
    @staticmethod
    def update_customer(
        customer_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None
    ) -> bool:
        """Update a customer"""
        updates = []
        params = []
        
        if first_name is not None:
            updates.append("first_name = %s")
            params.append(first_name)
        if last_name is not None:
            updates.append("last_name = %s")
            params.append(last_name)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if phone is not None:
            updates.append("phone = %s")
            params.append(phone)
        if address is not None:
            updates.append("address = %s")
            params.append(address)
        if city is not None:
            updates.append("city = %s")
            params.append(city)
        if country is not None:
            updates.append("country = %s")
            params.append(country)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(customer_id)
        
        query = f"UPDATE customers SET {', '.join(updates)} WHERE id = %s;"
        
        try:
            postgres_client.execute_update(query, tuple(params))
            logger.info(f"Customer {customer_id} updated")
            return True
        except Exception as error:
            logger.error(f"Error updating customer: {error}")
            raise
    
    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        """Delete a customer"""
        query = "DELETE FROM customers WHERE id = %s;"
        
        try:
            postgres_client.execute_update(query, (customer_id,))
            logger.info(f"Customer {customer_id} deleted")
            return True
        except Exception as error:
            logger.error(f"Error deleting customer: {error}")
            raise
    
    @staticmethod
    def get_customer_by_email(email: str) -> Optional[Customer]:
        """Get a customer by email"""
        query = """
            SELECT id, first_name, last_name, email, phone, address, city, country,
                   created_at, updated_at
            FROM customers
            WHERE email = %s;
        """
        try:
            result = postgres_client.execute_query(query, (email,), fetch_one=True)
            if result:
                return Customer(**result)
            return None
        except Exception as error:
            logger.error(f"Error getting customer by email: {error}")
            raise
    
    @staticmethod
    def search_customers(query_string: str) -> List[Customer]:
        """Search customers by name or email"""
        query = """
            SELECT id, first_name, last_name, email, phone, address, city, country,
                   created_at, updated_at
            FROM customers
            WHERE CONCAT(first_name, ' ', last_name) ILIKE %s
               OR email ILIKE %s
            ORDER BY created_at DESC;
        """
        search_pattern = f"%{query_string}%"
        
        try:
            results = postgres_client.execute_query(query, (search_pattern, search_pattern), fetch_all=True)
            return [Customer(**row) for row in results] if results else []
        except Exception as error:
            logger.error(f"Error searching customers: {error}")
            raise


# Singleton instance
customer_ops = CustomerOperations()

