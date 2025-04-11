# bridge/trading_bridge.py
from order_management.order_manager import OrderManager, OrderConfig
from trading_platforms.alpaca_manager import AlpacaManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingBridge:
    """
    Connects the OrderManager with the AlpacaManager to execute trades
    """

    def __init__(self, order_manager: OrderManager, alpaca_manager: AlpacaManager):
        self.order_manager = order_manager
        self.alpaca_manager = alpaca_manager
        logger.info("Trading Bridge initialized")

    def place_order(self, ticker_id: int, symbol: str, quantity: float, side: str, price: float) -> str:
        """
        Places an order using the AlpacaManager and tracks it in the OrderManager

        Args:
            ticker_id: Internal ticker ID
            symbol: Stock symbol (e.g., 'AAPL')
            quantity: Number of shares
            side: 'buy' or 'sell'
            price: Order price

        Returns:
            str: Alpaca order ID

        Raises:
            ValueError: If any parameters are invalid
            Exception: If order placement fails
        """
        # Validate inputs
        if side.lower() not in ('buy', 'sell'):
            raise ValueError(f"Invalid order side: {side}. Must be 'buy' or 'sell'")

        if quantity <= 0:
            raise ValueError(f"Invalid quantity: {quantity}. Must be greater than 0")

        if price <= 0:
            raise ValueError(f"Invalid price: {price}. Must be greater than 0")

        # 1. Create order in OrderManager
        order_config = OrderConfig(
            ticker_id=ticker_id,
            order_quantity=quantity,
            order_price=price
        )
        order = self.order_manager.add_order(order_config)
        logger.info(f"Created order #{order.order_number} in OrderManager")

        # 2. Place order with AlpacaManager
        try:
            alpaca_order_id = self.alpaca_manager.place_market_order(symbol, quantity, side)
            logger.info(f"Order {order.order_number} placed with Alpaca, Alpaca ID: {alpaca_order_id}")
            return alpaca_order_id
        except Exception as e:
            logger.error(f"Error placing order with Alpaca: {e}")
            # TODO: Add cleanup/rollback of OrderManager order
            raise