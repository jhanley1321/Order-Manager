# c:\Data_Tools\Order_Manager\main.py
import json
import os
from datetime import datetime
from order_manager import OrderManager, OrderConfig, OrderStatus, Order, OrderFill
from front_end import run_order_manager_app

def main():
    # Create an instance of OrderManager
    manager = OrderManager(data_folder="Data")

    # Define some order configurations
    orders_to_process = [
        OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00, exchange_id=1),
        OrderConfig(ticker_id=1002, order_quantity=200, order_price=75.00, exchange_id=2),
        OrderConfig(ticker_id=1003, order_quantity=150, order_price=60.00, exchange_id=3)
    ]

    # Add orders to the manager
    for order_config in orders_to_process:
        manager.add_order(order_config)

    # Fill some orders
    manager.fill_order(1, 49.95, 60)  # Partial fill
    manager.fill_order(1, 50.05, 40)  # Complete the order
    manager.fill_order(2, 74.50, 100)  # Partial fill
    manager.fill_order(3, 60.00, 150)  # Complete the order

    # List all orders
    manager.list_orders()

    # Save orders to a file
    manager.save_orders("orders.json")

    # Load orders from a file
    manager.load_orders("orders.json")

    # List all orders again to verify loading
    manager.list_orders()





if __name__ == '__main__':
    # main()
    run_order_manager_app()