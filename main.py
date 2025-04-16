# main.py
import json
import os
from datetime import datetime
from order_manager import OrderManager, OrderConfig, OrderStatus, Order, OrderFill
from interactive_demo import run_interactive_demo



def main():
    """
    Main function to demonstrate the OrderManager functionality
    """
    print("Order Manager Demo")
    print("-----------------\n")
    
    # Run the interactive demo
    run_interactive_demo()
    
    print("\nOrder Manager Demo completed")

if __name__ == "__main__":
    main()