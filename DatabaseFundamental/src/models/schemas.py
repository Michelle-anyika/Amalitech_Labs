"""
Data models and schemas for the e-commerce platform
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Customer:
    """Customer model"""
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Product:
    """Product model with JSONB metadata"""
    id: int
    name: str
    category_id: int
    price: float
    stock_quantity: int
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Metadata typically includes:
    # {
    #     "sizes": ["S", "M", "L", "XL"],
    #     "colors": ["red", "blue", "green"],
    #     "brand": "BrandName",
    #     "weight": "500g",
    #     "dimensions": {"length": 10, "width": 5, "height": 15}
    # }


@dataclass
class Category:
    """Product category model"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Order:
    """Order model"""
    id: int
    customer_id: int
    order_date: datetime
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OrderItem:
    """Individual line item in an order"""
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    created_at: Optional[datetime] = None

    def calculate_subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class OrderStatusHistory:
    """Track order status changes"""
    id: int
    order_id: int
    status: OrderStatus
    changed_at: datetime
    notes: Optional[str] = None


@dataclass
class UserSession:
    """User session data stored in MongoDB"""
    user_id: int
    session_id: str
    data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ShoppingCart:
    """Shopping cart stored in MongoDB"""
    user_id: int
    items: List[Dict[str, Any]]
    total_items: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Cart items format:
    # [
    #     {
    #         "product_id": 1,
    #         "product_name": "Product Name",
    #         "quantity": 2,
    #         "unit_price": 29.99,
    #         "subtotal": 59.98
    #     }
    # ]


@dataclass
class UserBehavior:
    """User behavior/event tracking stored in MongoDB"""
    user_id: int
    event_type: str
    event_data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Event types: "view", "add_to_cart", "remove_from_cart", "purchase", etc.


@dataclass
class TopProduct:
    """Top selling product (from cache)"""
    product_id: int
    product_name: str
    total_sales: int
    revenue: float
    rank: int

