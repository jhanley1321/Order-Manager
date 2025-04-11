import os
import logging
from order_management.order_manager import OrderManager
from trading_platforms.alpaca_manager import AlpacaManager, AlpacaConfig
from bridge.trading_bridge import TradingBridge

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_alpaca_manager():
    """
    Initialize and return the AlpacaManager with configuration.
    """
    # Get Alpaca credentials from environment variables
    api_key = os.getenv('ALPACA_MARKETS_API_KEY_TEST')
    secret_key = os.getenv('ALPACA_MARKETS_SECRET_KEY_TEST')

    if not api_key or not secret_key:
        raise ValueError("Alpaca API keys not found in environment variables")

    # Initialize AlpacaManager
    alpaca_config = AlpacaConfig(
        api_key=api_key,
        secret_key=secret_key,
        paper_trading=True
    )
    alpaca_manager = AlpacaManager(alpaca_config)
    logger.info("AlpacaManager initialized")
    return alpaca_manager

async def main():
    """
    Main async function that orchestrates the trading system.
    """
    order_manager = OrderManager()
    try:
        alpaca_manager = initialize_alpaca_manager()
        trading_bridge = TradingBridge(order_manager, alpaca_manager)
        logger.info("TradingBridge initialized")

        # Example: Place an order
        alpaca_order_id = trading_bridge.place_order(
            ticker_id=1001,
            symbol="AAPL",
            quantity=1,
            side="buy",
            price=150.00
        )
        logger.info(f"Order placed successfully, Alpaca order ID: {alpaca_order_id}")

    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        order_manager.save_orders()
        logger.info("Orders saved successfully")

def run():
    """
    Entry point for the application.
    """
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application shutdown by user")
    except Exception as e:
        logger.error(f"Application error: {e}")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    run()