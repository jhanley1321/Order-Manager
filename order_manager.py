from dataclasses import dataclass
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OrderConfig:
    """Configuration for creating trading orders"""
    asset_name: str = ""
    asset_type: str = ""
    asset_pair: str = ""
    order_quantity: float = 0.0
    order_price: float = 0.0
    base_currency: str = ""


class Order:
    """Represents a single trading order"""

    def __init__(self, order_number: int, config: OrderConfig):
        self.order_number = order_number
        self.config = config
        logger.info(f"Order #{self.order_number} created")

    def __del__(self):
        logger.info(f"Order #{self.order_number} destroyed")

    @property
    def asset_name(self) -> str:
        return self.config.asset_name

    @property
    def asset_type(self) -> str:
        return self.config.asset_type

    @property
    def asset_pair(self) -> str:
        return self.config.asset_pair

    @property
    def quantity(self) -> float:
        return self.config.order_quantity

    @property
    def order_price(self) -> float:
        return self.config.order_price

    @property
    def base_currency(self) -> str:
        return self.config.base_currency


class OrderManager:
    """Manages a collection of trading orders"""

    def __init__(self):
        self.orders: List[Order] = []
        self.next_order_number = 1
        logger.info("OrderManager created")

    def __del__(self):
        logger.info("OrderManager destroyed")

    def add_order(self, config: OrderConfig) -> None:
        """Creates and adds a new order with the given configuration"""
        new_order = Order(self.next_order_number, config)
        self.orders.append(new_order)
        logger.info(f"Added Order #{self.next_order_number}")
        self.next_order_number += 1

    def get_order(self, order_number: int) -> Order:
        """Retrieves an order by its order number"""
        for order in self.orders:
            if order.order_number == order_number:
                return order
        raise ValueError(f"Order #{order_number} not found")

    def list_orders(self) -> None:
        """Prints all current orders"""
        for order in self.orders:
            print(f"Order #{order.order_number}:")
            print(f"  Asset: {order.asset_name} ({order.asset_type})")
            print(f"  Pair: {order.asset_pair}")
            print(f"  Quantity: {order.quantity}")
            print(f"  Price: {order.order_price} {order.base_currency}")
            print()