# main.py
from order_manager import OrderManager, OrderConfig, OrderStatus

def main():
    """
    Main function to demonstrate the OrderManager functionality
    """
    print("Order Manager Demo")
    print("-----------------\n")
    
    # Create an order manager
    manager = OrderManager()
    
    # Create some sample orders
    orders = [
        OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.25),
        OrderConfig(ticker_id=1002, order_quantity=200, order_price=75.50),
        OrderConfig(ticker_id=1003, order_quantity=150, order_price=32.75)
    ]
    
    # Add orders to the manager
    added_orders = []
    print("Creating orders...")
    for config in orders:
        order = manager.add_order(config)
        added_orders.append(order)
        print(f"Created Order #{order.order_number}: {order.quantity} shares of ticker {order.ticker_id} @ ${order.order_price:.2f}")
    
    print("\nList of all orders:")
    manager.list_orders()
    
    # Fill some orders
    print("\nFilling orders...")
    
    # Partially fill the first order
    order1 = added_orders[0]
    fill_price1 = order1.order_price - 0.15  # Fill slightly below order price
    fill_qty1 = order1.quantity * 0.6  # Fill 60% of the order
    manager.fill_order(order1.order_number, fill_price1, fill_qty1)
    print(f"Filled {fill_qty1} shares of Order #{order1.order_number} @ ${fill_price1:.2f}")
    
    # Complete the fill for the first order
    fill_price2 = order1.order_price + 0.10  # Fill slightly above order price
    fill_qty2 = order1.remaining_quantity  # Fill the rest
    manager.fill_order(order1.order_number, fill_price2, fill_qty2)
    print(f"Filled {fill_qty2} shares of Order #{order1.order_number} @ ${fill_price2:.2f}")
    
    # Partially fill the second order
    order2 = added_orders[1]
    fill_price3 = order2.order_price - 0.25
    fill_qty3 = order2.quantity * 0.4  # Fill 40% of the order
    manager.fill_order(order2.order_number, fill_price3, fill_qty3)
    print(f"Filled {fill_qty3} shares of Order #{order2.order_number} @ ${fill_price3:.2f}")
    
    # Display the updated orders
    print("\nUpdated list of all orders:")
    manager.list_orders()
    
    # Show open orders
    open_orders = manager.get_open_orders()
    print(f"\nThere are {len(open_orders)} open orders remaining")
    for order in open_orders:
        print(f"Order #{order.order_number}: {order.remaining_quantity} shares remaining to fill")
    
    # Save orders to disk
    manager.save_orders()
    print("\nOrders saved to disk")
    
    print("\nOrder Manager Demo completed")

if __name__ == "__main__":
    main()