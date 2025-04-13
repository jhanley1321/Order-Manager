# main.py
import json
import os
from datetime import datetime
from order_manager import OrderManager, OrderConfig, OrderStatus, Order, OrderFill
from interactive_demo import run_interactive_demo

# def interactive_demo():
#     """Interactive version of the order manager demo"""
#     # Create an order manager
#     manager = OrderManager()
    
#     # Try to load previously saved orders
#     manager.load_orders()
    
#     while True:
#         print("\nOrder Manager Menu:")
#         print("1. List all orders")
#         print("2. Add new order")
#         print("3. Fill an existing order")
#         print("4. Show open orders")
#         print("5. Save and exit")
        
#         choice = input("\nEnter your choice (1-5): ")
        
#         if choice == '1':
#             print("\nList of all orders:")
#             manager.list_orders()
        
#         elif choice == '2':
#             try:
#                 ticker_id = int(input("Enter ticker ID: "))
#                 quantity = float(input("Enter order quantity: "))
#                 price = float(input("Enter order price: "))
                
#                 config = OrderConfig(ticker_id=ticker_id, order_quantity=quantity, order_price=price)
#                 order = manager.add_order(config)
                
#                 print(f"\nCreated Order #{order.order_number}: {order.quantity} shares of ticker {order.ticker_id} @ ${order.order_price:.2f}")
#             except ValueError:
#                 print("Invalid input! Order creation cancelled.")
        
#         elif choice == '3':
#             open_orders = manager.get_open_orders()
            
#             if not open_orders:
#                 print("No open orders to fill!")
#                 continue
            
#             # Display open orders
#             print("\nOpen orders that can be filled:")
#             for i, order in enumerate(open_orders):
#                 print(f"{i+1}. Order #{order.order_number}: {order.remaining_quantity} shares of ticker {order.ticker_id} remaining @ ${order.order_price:.2f}")
            
#             # Allow user to select order to fill
#             try:
#                 selection = int(input("\nSelect an order to fill (number): ")) - 1
#                 if 0 <= selection < len(open_orders):
#                     order = open_orders[selection]
                    
#                     # Get fill details
#                     try:
#                         fill_price = float(input(f"Enter fill price (current price: ${order.order_price:.2f}): "))
#                         max_fill = order.remaining_quantity
#                         fill_qty = float(input(f"Enter fill quantity (max: {max_fill}): "))
                        
#                         if 0 < fill_qty <= max_fill:
#                             manager.fill_order(order.order_number, fill_price, fill_qty)
#                             print(f"Filled {fill_qty} shares of Order #{order.order_number} @ ${fill_price:.2f}")
#                         else:
#                             print("Invalid fill quantity!")
#                     except ValueError:
#                         print("Invalid input! Fill operation cancelled.")
#                 else:
#                     print("Invalid selection!")
#             except ValueError:
#                 print("Invalid input! No order filled.")
        
#         elif choice == '4':
#             open_orders = manager.get_open_orders()
#             print(f"\nThere are {len(open_orders)} open orders remaining")
#             for order in open_orders:
#                 print(f"Order #{order.order_number}: {order.remaining_quantity} shares of ticker {order.ticker_id} remaining @ ${order.order_price:.2f}")
        
#         elif choice == '5':
#             # Save orders to disk
#             manager.save_orders()
#             print("\nOrders saved to disk")
#             print("Exiting Order Manager Demo")
#             break
        
#         else:
#             print("Invalid choice! Please enter a number between 1 and 5.")

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