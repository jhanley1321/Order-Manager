# trading_platforms/alpaca_manager.py
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AlpacaConfig:
    """Configuration for Alpaca trading"""
    api_key: str
    secret_key: str
    paper_trading: bool = True

class AlpacaManager:
    """Manages trading operations with Alpaca"""

    def __init__(self, config: AlpacaConfig):
        self.trading_client = TradingClient(
            api_key=config.api_key,
            secret_key=config.secret_key,
            paper=config.paper_trading
        )
        logger.info("Alpaca Manager initialized")

    def place_market_order(self, symbol: str, quantity: float, side: str) -> str:
        """
        Place a market order for a given symbol

        Args:
            symbol: The stock symbol (e.g., 'AAPL')
            quantity: Number of shares to trade
            side: 'buy' or 'sell'

        Returns:
            str: Alpaca order ID
        """
        # Validate side
        side = side.lower()
        if side not in ('buy', 'sell'):
            raise ValueError("Side must be 'buy' or 'sell'")

        # Create the market order request
        market_order = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.BUY if side == 'buy' else OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )

        # Submit the order
        try:
            order = self.trading_client.submit_order(market_order)
            logger.info(f"Placed {side} order for {quantity} shares of {symbol}")
            return order.id
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise

    # Testing 
    def get_order_status(self, alpaca_order_id: str) -> dict:
            """
            Fetch the status of an order from Alpaca.

            Args:
                alpaca_order_id: The ID of the order in Alpaca.

            Returns:
                dict: A dictionary containing the order status, filled quantity, and average fill price.
            """
            try:
                order = self.trading_client.get_order_by_id(alpaca_order_id)
                return {
                    "status": order.status,  # e.g., 'filled', 'partially_filled'
                    "filled_qty": float(order.filled_qty),
                    "avg_fill_price": float(order.filled_avg_price) if order.filled_avg_price else 0.0
                }
            except Exception as e:
                logger.error(f"Error fetching order status from Alpaca: {e}")
                raise