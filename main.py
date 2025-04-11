# main.py
from order_management.order_manager import OrderManager, OrderConfig
from trading_platforms.alpaca_manager import AlpacaManager, AlpacaConfig
from bridge.trading_bridge import TradingBridge
import os

def main():
    # 1. Initialize components
    order_manager = OrderManager()

    alpaca_config = AlpacaConfig(
        api_key=os.getenv('ALPACA_MARKETS_API_KEY_TEST'),
        secret_key=os.getenv('ALPACA_MARKETS_SECRET_KEY_TEST'),
        paper_trading=True
    )
    alpaca_manager = AlpacaManager(alpaca_config)

    trading_bridge = TradingBridge(order_manager, alpaca_manager)

    # 2. Place an order through the bridge
    try:
        alpaca_order_id = trading_bridge.place_order(
            ticker_id=1001,
            symbol="AAPL",
            quantity=1,
            side="buy",
            price=150.00  # Example price
        )
        print(f"Order placed successfully, Alpaca order ID: {alpaca_order_id}")

        # 3. Display orders
        order_manager.list_orders()
        order_manager.save_orders()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()