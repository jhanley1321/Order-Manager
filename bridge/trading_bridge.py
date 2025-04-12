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
        """
        # Validate inputs
        if side.lower() not in ('buy', 'sell'):
            raise ValueError(f"Invalid order side: {side}. Must be 'buy' or 'sell'")

        if quantity <= 0:
            raise ValueError(f"Invalid quantity: {quantity}. Must be greater than 0")

        if price <= 0:
            raise ValueError(f"Invalid price: {price}. Must be greater than 0")

        # Create order in OrderManager
        order_config = OrderConfig(
            ticker_id=ticker_id,
            order_quantity=quantity,
            order_price=price
        )
        order = self.order_manager.add_order(order_config)
        logger.info(f"Created order #{order.order_number} in OrderManager")

        # Place order with AlpacaManager
        try:
            alpaca_order_id = self.alpaca_manager.place_market_order(symbol, quantity, side)
            logger.info(f"Order {order.order_number} placed with Alpaca, Alpaca ID: {alpaca_order_id}")
            return alpaca_order_id
        except Exception as e:
            logger.error(f"Error placing order with Alpaca: {e}")
            raise

    def update_order_status(self, alpaca_order_id: str) -> None:
        """
        Update the status of an order in the OrderManager based on Alpaca's order status
        """
        try:
            # Fetch order status from Alpaca
            alpaca_status = self.alpaca_manager.get_order_status(alpaca_order_id)

            # Find the corresponding order in the OrderManager
            order = next(
                (o for o in self.order_manager.orders if o.order_number == int(alpaca_order_id)),
                None
            )

            if not order:
                logger.warning(f"No matching order found in OrderManager for Alpaca ID: {alpaca_order_id}")
                return

            # Update the order based on status
            if alpaca_status["status"] == "filled":
                order.add_fill(
                    price=alpaca_status["avg_fill_price"],
                    quantity=alpaca_status["filled_qty"]
                )
            elif alpaca_status["status"] == "partially_filled":
                new_fill_quantity = alpaca_status["filled_qty"] - order.filled_quantity
                if new_fill_quantity > 0:
                    order.add_fill(
                        price=alpaca_status["avg_fill_price"],
                        quantity=new_fill_quantity
                    )

            logger.info(f"Order #{order.order_number} updated with status: {order.status}")

        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            raise