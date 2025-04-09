from order_manager import OrderManager, OrderConfig

def main():
    # Create an order manager
    manager = OrderManager()

    # Create a Bitcoin order configuration
    config = OrderConfig(
        asset_name="Bitcoin",
        asset_type="Crypto",
        asset_pair="BTC/USD",
        order_quantity=0.5,
        order_price=50000.00,
        base_currency="USD"
    )

    # Add the order and display all orders
    manager.add_order(config)

    # Add another order for demonstration
    eth_config = OrderConfig(
        asset_name="Ethereum",
        asset_type="Crypto",
        asset_pair="ETH/USD",
        order_quantity=2.0,
        order_price=3000.00,
        base_currency="USD"
    )
    manager.add_order(eth_config)

    # List all orders
    print("\nCurrent Orders:")
    manager.list_orders()

if __name__ == "__main__":
    main()