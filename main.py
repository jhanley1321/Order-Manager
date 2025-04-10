from order_manager import OrderManager, OrderConfig

def main():
    # Create order manager (will create Data folder if it doesn't exist)
    manager = OrderManager()

    # Create and add first order
    order1_config = OrderConfig(
        ticker_id=1001,
        order_quantity=100,
        order_price=50.00
    )
    manager.add_order(order1_config)

    # Create and add second order
    order2_config = OrderConfig(
        ticker_id=2001,
        order_quantity=200,
        order_price=75.00
    )
    manager.add_order(order2_config)

    # Add fills to first order until it's complete
    manager.fill_order(order_number=1, fill_price=49.95, fill_quantity=60)
    manager.fill_order(order_number=1, fill_price=50.05, fill_quantity=40)  # This will complete the order

    # Try to add another fill to the completed order (will be ignored)
    manager.fill_order(order_number=1, fill_price=50.10, fill_quantity=10)

    # Add partial fill to second order
    manager.fill_order(order_number=2, fill_price=74.95, fill_quantity=100)

    # Display final order status
    print("\nAll Orders:")
    manager.list_orders()

    # Display only orders that still need fills
    open_orders = manager.get_open_orders()
    print("\nOrders still needing fills:")
    for order in open_orders:
        print(f"Order #{order.order_number} - {order.status.value} - Remaining: {order.remaining_quantity}")

    # Save orders to file at the end of the session
    manager.save_orders()

if __name__ == "__main__":
    main()