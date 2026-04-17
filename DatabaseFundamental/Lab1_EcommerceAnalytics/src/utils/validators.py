"""
Data validation utilities
"""
import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class Validators:
    """Data validation utilities"""

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format

        Returns:
            (is_valid, error_message)
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, ""

    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        """Validate price is positive"""
        if price < 0:
            return False, "Price cannot be negative"
        return True, ""

    @staticmethod
    def validate_quantity(quantity: int) -> Tuple[bool, str]:
        """Validate quantity is positive"""
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        return True, ""

    @staticmethod
    def validate_customer_name(name: str) -> Tuple[bool, str]:
        """Validate customer name"""
        if not name or len(name.strip()) == 0:
            return False, "Name cannot be empty"
        if len(name) > 100:
            return False, "Name too long (max 100 characters)"
        return True, ""

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number"""
        pattern = r'^\+?1?\d{9,15}$'
        if phone and not re.match(pattern, phone):
            return False, "Invalid phone number format"
        return True, ""


# Singleton instance
validators = Validators()

