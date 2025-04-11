# tests/test_trading_bridge.py
import unittest
from unittest.mock import Mock, patch
from order_management.order_manager import OrderManager, OrderConfig, Order
from trading_platforms.alpaca_manager import AlpacaManager
from bridge.trading_bridge import TradingBridge

class TestTradingBridge(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock managers
        self.order_manager = Mock(spec=OrderManager)
        self.alpaca_manager = Mock(spec=AlpacaManager)

        # Create the bridge with mock managers
        self.bridge = TradingBridge(self.order_manager, self.alpaca_manager)

        # Common test data
        self.test_ticker_id = 1001
        self.test_symbol = "AAPL"
        self.test_quantity = 100
        self.test_price = 150.00
        self.test_side = "buy"

    def test_place_order_success(self):
        """Test successful order placement"""
        # Setup mock returns
        mock_order = Mock(spec=Order)
        mock_order.order_number = 1
        self.order_manager.add_order.return_value = mock_order
        self.alpaca_manager.place_market_order.return_value = "test_alpaca_order_id"

        # Place order through bridge
        alpaca_order_id = self.bridge.place_order(
            ticker_id=self.test_ticker_id,
            symbol=self.test_symbol,
            quantity=self.test_quantity,
            side=self.test_side,
            price=self.test_price
        )

        # Verify OrderManager interaction
        self.order_manager.add_order.assert_called_once()
        order_config = self.order_manager.add_order.call_args[0][0]
        self.assertEqual(order_config.ticker_id, self.test_ticker_id)
        self.assertEqual(order_config.order_quantity, self.test_quantity)
        self.assertEqual(order_config.order_price, self.test_price)

        # Verify AlpacaManager interaction
        self.alpaca_manager.place_market_order.assert_called_once_with(
            self.test_symbol,
            self.test_quantity,
            self.test_side
        )

        # Verify return value
        self.assertEqual(alpaca_order_id, "test_alpaca_order_id")

    def test_place_order_alpaca_failure(self):
        """Test handling of Alpaca order placement failure"""
        # Setup mock returns
        mock_order = Mock(spec=Order)
        mock_order.order_number = 1
        self.order_manager.add_order.return_value = mock_order
        self.alpaca_manager.place_market_order.side_effect = Exception("Alpaca API Error")

        # Attempt to place order and verify exception is raised
        with self.assertRaises(Exception) as context:
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=self.test_quantity,
                side=self.test_side,
                price=self.test_price
            )

        # Verify the exception message
        self.assertTrue("Alpaca API Error" in str(context.exception))

        # Verify OrderManager was still called
        self.order_manager.add_order.assert_called_once()

    def test_invalid_side(self):
        """Test handling of invalid order side"""
        # Attempt to place order with invalid side
        with self.assertRaises(ValueError):
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=self.test_quantity,
                side="invalid_side",
                price=self.test_price
            )

        # Verify no interactions with managers
        self.order_manager.add_order.assert_not_called()
        self.alpaca_manager.place_market_order.assert_not_called()

    def test_zero_quantity(self):
        """Test handling of zero quantity orders"""
        with self.assertRaises(ValueError):
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=0,
                side=self.test_side,
                price=self.test_price
            )

        # Verify no interactions with managers
        self.order_manager.add_order.assert_not_called()
        self.alpaca_manager.place_market_order.assert_not_called()

    def test_negative_price(self):
        """Test handling of negative price orders"""
        with self.assertRaises(ValueError):
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=self.test_quantity,
                side=self.test_side,
                price=-1.0
            )

        # Verify no interactions with managers
        self.order_manager.add_order.assert_not_called()
        self.alpaca_manager.place_market_order.assert_not_called()

if __name__ == '__main__':
    unittest.main()