# order_manager.py
from dataclasses import dataclass
from typing import List
import logging
from datetime import datetime
import json
import os
import pathlib
from enum import Enum
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderStatus(Enum):
    """Enum for order status"""
    OPEN = "Open"
    PARTIALLY_FILLED = "Partially Filled"
    FILLED = "Filled"
   

@dataclass
class OrderDetails:
    """Details for creating trading orders"""
    ticker_id: int = 0
    order_quantity: float = 0.0
    order_price: float = 0.0
    exchange_id: int = 0
    transaction_fee: float = 0.0


@dataclass
class OrderFill:
    """Represents a single fill for an order"""
    fill_price: float
    fill_quantity: float
    filled_at: datetime = datetime.now()

class Order:
    """Represents a single trading order"""

    # Constructor creates an order wtih the given details 
    def __init__(self, details: OrderDetails):
        self.details = details
        self.created_at = datetime.now() # Logs when the 
        self.fills: List[OrderFill] = [] # List of fills, by default there are no fills until they are filled. 
        self._status = OrderStatus.OPEN # By default, all orders are open until filled. 
        logger.info(f"Order created with status: {self._status.value} and transaction fee: {self.details.transaction_fee}") # Logs when the object is created

    # Destructor: Destoryts the object 
    def __del__(self):
        logger.info("Order destroyed")

    @property # Getter
    def status(self) -> OrderStatus:
        """Returns the current status of the order"""
        return self._status

    @property # Getter
    def is_filled(self) -> bool:
        """Returns True if the order is completely filled"""
        return self._status == OrderStatus.FILLED

    @property # Getter
    def needs_fills(self) -> bool:
        """Returns True if the order still needs fills"""
        return self._status != OrderStatus.FILLED

    @property # Getter
    def filled_quantity(self) -> float:
        """Returns the total quantity filled so far"""
        return sum(fill.fill_quantity for fill in self.fills)

    @property # Getter
    def remaining_quantity(self) -> float:
        """Returns the remaining quantity to be filled"""
        return self.quantity - self.filled_quantity

    @property # Getter
    def average_fill_price(self) -> float:
        """Returns the weighted average fill price"""
        if not self.fills:
            return 0.0
        total_value = sum(fill.fill_price * fill.fill_quantity for fill in self.fills)
        return total_value / self.filled_quantity

    @property # Getter
    def ticker_id(self) -> int:
        return self.details.ticker_id

    @property # Getter
    def quantity(self) -> float:
        return self.details.order_quantity

    @property # Getter
    def order_price(self) -> float:
        return self.details.order_price

    @property # Getter
    def exchange_id(self) -> int:
        return self.details.exchange_id

    @property
    def transaction_fee(self) -> float:
        """Returns the transaction fee for the order"""
        return self.details.transaction_fee

    # Updates the status on an order
    def _update_status(self) -> None:
        """Updates the order status based on fills"""
        if self.filled_quantity >= self.quantity:
            self._status = OrderStatus.FILLED
            logger.info(f"Order is now completely filled")
        elif self.fills:
            self._status = OrderStatus.PARTIALLY_FILLED
        else:
            self._status = OrderStatus.OPEN

    # Adds a fill to the order 
    def add_fill(self, price: float, quantity: float) -> None:
        """Adds a new fill to the order"""
        if not self.needs_fills:
            raise ValueError("Order is already completely filled")

        if quantity > self.remaining_quantity:
            raise ValueError(f"Fill quantity ({quantity}) exceeds remaining quantity ({self.remaining_quantity})")

        fill = OrderFill(price, quantity)
        self.fills.append(fill)
        self._update_status()
        logger.info(f"Order received fill: {quantity} @ {price}. Status: {self._status.value}")

class OrderManager:
    """Manages a collection of trading orders"""

    
    def __init__(self, data_folder: str = "data"):
        self.orders: List[Order] = []
        self.next_order_number = 1  # Default to 1 for new instances with no orders
        self.data_folder = data_folder
        self._ensure_data_folder_exists()
        logger.info("OrderManager created")

        # Automatically load orders when creating the manager
        # This ensures we have the correct next_order_number right from initialization
        self.load_orders()

    def __del__(self):
        logger.info("OrderManager destroyed")

    def _ensure_data_folder_exists(self) -> None:
        """Ensures the data folder exists, creates it if it doesn't"""
        pathlib.Path(self.data_folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Using data folder: {self.data_folder}")

    def add_order(self, details: OrderDetails) -> Order:
        """Creates and adds a new order with the given detailsuration"""
        new_order = Order(details)
        self.orders.append(new_order)
        logger.info(f"Added Order #{self.next_order_number} with transaction fee: {details.transaction_fee}")
        self.next_order_number += 1
        return new_order

    def get_order(self, order_number: int) -> Order:
        """Retrieves an order by its order number"""
        for order in self.orders:
            if order_number == self.orders.index(order) + 1:
                return order
        raise ValueError(f"Order #{order_number} not found")

    def append_orders(self, filename: str = "orders.json") -> None:
        """Appends current orders to existing JSON file"""
        file_path = os.path.join(self.data_folder, filename)
        existing_orders = []

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_orders = json.load(file)

        orders_data = []
        for order in self.orders:
            order_data = {
                "order_number": self.orders.index(order) + 1,
                "ticker_id": order.ticker_id,
                "exchange_id": order.exchange_id,
                "original_quantity": order.quantity,
                "order_price": order.order_price,
                "created_at": str(order.created_at),
                "status": order.status.value,
                "needs_fills": order.needs_fills,
                "filled_quantity": order.filled_quantity,
                "remaining_quantity": order.remaining_quantity,
                "average_fill_price": order.average_fill_price,
                "transaction_fee": order.transaction_fee,
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

        existing_orders.extend(orders_data)

        with open(file_path, 'w') as file:
            json.dump(existing_orders, file, indent=4)
            logger.info(f"Orders appended to {file_path}")

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
            order_number = self.orders.index(order) + 1
            print(f"\nOrder #{order_number}:")
            print(f"  Ticker ID: {order.ticker_id}")
            print(f"  Exchange ID: {order.exchange_id}")
            print(f"  Original Quantity: {order.quantity}")
            print(f"  Order Price: {order.order_price}")
            print(f"  Created At: {order.created_at}")
            print(f"  Transaction Fee: {order.transaction_fee}")
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
                "order_number": self.orders.index(order) + 1,
                "ticker_id": order.ticker_id,
                "exchange_id": order.exchange_id,
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

    def load_orders(self, filename: str = "orders.json") -> bool:
        """
        Load orders from a JSON file in the data folder

        Args:
        filename: The name of the JSON file containing saved orders

        Returns:
        bool: True if orders were loaded, False otherwise
        """
        file_path = os.path.join(self.data_folder, filename)

        if not os.path.exists(file_path):
            logger.info(f"No saved orders file found at {file_path}")
            return False

        try:
            with open(file_path, 'r') as file:
                orders_data = json.load(file)

            logger.info(f"Loading {len(orders_data)} previously saved orders...")

            # Find the highest order number in the saved orders
            highest_order_num = 0

            for order_data in orders_data:
                details = OrderDetails(
                    ticker_id=order_data["ticker_id"],
                    order_quantity=order_data["original_quantity"],
                    order_price=order_data["order_price"],
                    exchange_id=order_data["exchange_id"],
                    transaction_fee=order_data["transaction_fee"]
                )

                # Create a new order with the saved order number
                new_order = Order(details)

                # Add fills by directly adding to the fills list
                for fill_data in order_data["fills"]:
                    fill_price = fill_data["fill_price"]
                    fill_quantity = fill_data["fill_quantity"]

                    # Add fill directly to the list to bypass validation
                    new_order.fills.append(OrderFill(fill_price, fill_quantity))

                # Force status update
                new_order._update_status()

                # Add the order to our manager
                self.orders.append(new_order)

                # Keep track of the highest order number
                highest_order_num = max(highest_order_num, order_data["order_number"])

            # Set the next order number
            self.next_order_number = highest_order_num + 1
            logger.info(f"Successfully loaded {len(orders_data)} orders.")
            logger.info(f"Next order number will be {self.next_order_number}")
            return True

        except Exception as e:
            logger.error(f"Error loading orders: {e}")
            return False

    def get_orders_as_dataframe(self, filename: str = "orders.json") -> pd.DataFrame:
        """
        Args:
        filename: The name of the JSON file containing saved orders
        
        Returns:
        pd.DataFrame: pandas data frame of the orders by  reading from the JSON file
        
        """
        file_path = os.path.join(self.data_folder, filename)

        if not os.path.exists(file_path):
            logger.warning(f"No saved orders file found at {file_path}")
            return pd.DataFrame()

        try:
            with open(file_path, 'r') as file:
                orders_data = json.load(file)

            orders_df = pd.DataFrame(orders_data)
            orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])
            for idx, row in orders_df.iterrows():
                if row['fills']:
                    orders_df.at[idx, 'fills'] = pd.DataFrame(row['fills'])

            return orders_df

        except Exception as e:
            logger.error(f"Error converting orders to DataFrame: {e}")
            return pd.DataFrame()

def run_order_manager(orders_to_process: List[OrderDetails]) -> OrderManager:
    """
    Wrapper function to run the order manager with a list of orders

    Args:
    orders_to_process: List of OrderDetails objects to process

    Returns:
    OrderManager: The manager instance with processed orders
    """
    manager = OrderManager()

    for order_details in orders_to_process:
        manager.add_order(order_details)

    return manager