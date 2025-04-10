from dataclasses import dataclass
from typing import List
import logging
from datetime import datetime
import json
import os
import pathlib
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderStatus(Enum):
    """Enum for order status"""
    OPEN = "Open"
    PARTIALLY_FILLED = "Partially Filled"
    FILLED = "Filled"

@dataclass
class OrderConfig:
    """Configuration for creating trading orders"""
    ticker_id: int = 0
    order_quantity: float = 0.0
    order_price: float = 0.0

@dataclass
class OrderFill:
    """Represents a single fill for an order"""
    fill_price: float
    fill_quantity: float
    filled_at: datetime = datetime.now()

class Order:
    """Represents a single trading order"""

    def __init__(self, order_number: int, config: OrderConfig):
        self.order_number = order_number
        self.config = config
        self.created_at = datetime.now()
        self.fills: List[OrderFill] = []
        self._status = OrderStatus.OPEN
        logger.info(f"Order #{self.order_number} created with status: {self._status.value}")

    def __del__(self):
        logger.info(f"Order #{self.order_number} destroyed")

    @property
    def status(self) -> OrderStatus:
        """Returns the current status of the order"""
        return self._status

    @property
    def is_filled(self) -> bool:
        """Returns True if the order is completely filled"""
        return self._status == OrderStatus.FILLED

    @property
    def needs_fills(self) -> bool:
        """Returns True if the order still needs fills"""
        return self._status != OrderStatus.FILLED

    @property
    def filled_quantity(self) -> float:
        """Returns the total quantity filled so far"""
        return sum(fill.fill_quantity for fill in self.fills)

    @property
    def remaining_quantity(self) -> float:
        """Returns the remaining quantity to be filled"""
        return self.quantity - self.filled_quantity

    @property
    def average_fill_price(self) -> float:
        """Returns the weighted average fill price"""
        if not self.fills:
            return 0.0
        total_value = sum(fill.fill_price * fill.fill_quantity for fill in self.fills)
        return total_value / self.filled_quantity

    @property
    def ticker_id(self) -> int:
        return self.config.ticker_id

    @property
    def quantity(self) -> float:
        return self.config.order_quantity

    @property
    def order_price(self) -> float:
        return self.config.order_price

    def _update_status(self) -> None:
        """Updates the order status based on fills"""
        if self.filled_quantity >= self.quantity:
            self._status = OrderStatus.FILLED
            logger.info(f"Order #{self.order_number} is now completely filled")
        elif self.fills:
            self._status = OrderStatus.PARTIALLY_FILLED
        else:
            self._status = OrderStatus.OPEN

    def add_fill(self, price: float, quantity: float) -> None:
        """Adds a new fill to the order"""
        if not self.needs_fills:
            raise ValueError(f"Order #{self.order_number} is already completely filled")

        if quantity > self.remaining_quantity:
            raise ValueError(f"Fill quantity ({quantity}) exceeds remaining quantity ({self.remaining_quantity})")

        fill = OrderFill(price, quantity)
        self.fills.append(fill)
        self._update_status()
        logger.info(f"Order #{self.order_number} received fill: {quantity} @ {price}. Status: {self._status.value}")

class OrderManager:
    """Manages a collection of trading orders"""

    def __init__(self, data_folder: str = "Data"):
        self.orders: List[Order] = []
        self.next_order_number = 1
        self.data_folder = data_folder
        self._ensure_data_folder_exists()
        logger.info("OrderManager created")

    def __del__(self):
        logger.info("OrderManager destroyed")

    def _ensure_data_folder_exists(self) -> None:
        """Ensures the data folder exists, creates it if it doesn't"""
        pathlib.Path(self.data_folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Using data folder: {self.data_folder}")

    def add_order(self, config: OrderConfig) -> Order:
        """Creates and adds a new order with the given configuration"""
        new_order = Order(self.next_order_number, config)
        self.orders.append(new_order)
        logger.info(f"Added Order #{self.next_order_number}")
        self.next_order_number += 1
        return new_order

    def get_order(self, order_number: int) -> Order:
        """Retrieves an order by its order number"""
        for order in self.orders:
            if order.order_number == order_number:
                return order
        raise ValueError(f"Order #{order_number} not found")

    def fill_order(self, order_number: int, fill_price: float, fill_quantity: float) -> None:
        """Adds a fill to an existing order"""
        order = self.get_order(order_number)
        if not order.needs_fills:
            logger.warning(f"Order #{order_number} is already filled, ignoring fill request")
            return
        order.add_fill(fill_price, fill_quantity)

    def get_open_orders(self) -> List[Order]:
        """Returns a list of orders that still need fills"""
        return [order for order in self.orders if order.needs_fills]

    def list_orders(self) -> None:
        """Prints all current orders"""
        for order in self.orders:
            print(f"\nOrder #{order.order_number}:")
            print(f"  Ticker ID: {order.ticker_id}")
            print(f"  Original Quantity: {order.quantity}")
            print(f"  Order Price: {order.order_price}")
            print(f"  Created At: {order.created_at}")
            print(f"  Status: {order.status.value}")
            print(f"  Needs Fills: {'Yes' if order.needs_fills else 'No'}")
            print(f"  Filled Quantity: {order.filled_quantity}")
            print(f"  Remaining Quantity: {order.remaining_quantity}")

            if order.fills:
                print("  Fill History:")
                for idx, fill in enumerate(order.fills, 1):
                    print(f"    Fill #{idx}: {fill.fill_quantity} @ {fill.fill_price} ({fill.filled_at})")
                print(f"  Average Fill Price: {order.average_fill_price}")

    def save_orders(self, filename: str = "orders.json") -> None:
        """Saves all orders to a JSON file in the data folder"""
        file_path = os.path.join(self.data_folder, filename)
        orders_data = []

        for order in self.orders:
            order_data = {
                "order_number": order.order_number,
                "ticker_id": order.ticker_id,
                "original_quantity": order.quantity,
                "order_price": order.order_price,
                "created_at": str(order.created_at),
                "status": order.status.value,
                "needs_fills": order.needs_fills,
                "filled_quantity": order.filled_quantity,
                "remaining_quantity": order.remaining_quantity,
                "average_fill_price": order.average_fill_price,
                "fills": [
                    {
                        "fill_price": fill.fill_price,
                        "fill_quantity": fill.fill_quantity,
                        "filled_at": str(fill.filled_at)
                    }
                    for fill in order.fills
                ]
            }
            orders_data.append(order_data)

        with open(file_path, 'w') as file:
            json.dump(orders_data, file, indent=4)
        logger.info(f"Orders saved to {file_path}")