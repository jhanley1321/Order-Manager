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
        self.mock_order_manager = Mock(spec=OrderManager)
        self.mock_alpaca_manager = Mock(spec=AlpacaManager)

        # Create the bridge with mock managers
        self.bridge = TradingBridge(self.mock_order_manager, self.mock_alpaca_manager)

        # Common test data
        self.test_ticker_id = 1001
        self.test_symbol = "AAPL"
        self.test_quantity = 100
        self.test_price = 150.00
        self.test_side = "buy"

    def test_initialization(self):
        """Test TradingBridge initialization"""
        self.assertIsNotNone(self.bridge)
        self.assertEqual(self.bridge.order_manager, self.mock_order_manager)
        self.assertEqual(self.bridge.alpaca_manager, self.mock_alpaca_manager)

    def test_place_order_success(self):
        """Test successful order placement"""
        # Setup mock returns
        mock_order = Mock()
        mock_order.order_number = 1
        self.mock_order_manager.add_order.return_value = mock_order
        self.mock_alpaca_manager.place_market_order.return_value = "test_alpaca_order_id"

        # Place order through bridge
        alpaca_order_id = self.bridge.place_order(
            ticker_id=self.test_ticker_id,
            symbol=self.test_symbol,
            quantity=self.test_quantity,
            side=self.test_side,
            price=self.test_price
        )

        # Verify OrderManager interaction
        self.mock_order_manager.add_order.assert_called_once()
        order_config = self.mock_order_manager.add_order.call_args[0][0]
        self.assertEqual(order_config.ticker_id, self.test_ticker_id)
        self.assertEqual(order_config.order_quantity, self.test_quantity)
        self.assertEqual(order_config.order_price, self.test_price)

        # Verify AlpacaManager interaction
        self.mock_alpaca_manager.place_market_order.assert_called_once_with(
            self.test_symbol,
            self.test_quantity,
            self.test_side
        )

        # Verify return value
        self.assertEqual(alpaca_order_id, "test_alpaca_order_id")

    def test_place_order_alpaca_failure(self):
        """Test handling of Alpaca order placement failure"""
        # Setup mock returns
        mock_order = Mock()
        mock_order.order_number = 1
        self.mock_order_manager.add_order.return_value = mock_order
        self.mock_alpaca_manager.place_market_order.side_effect = Exception("Alpaca API Error")

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
        self.mock_order_manager.add_order.assert_called_once()

    def test_invalid_side(self):
        """Test handling of invalid order side"""
        with self.assertRaises(ValueError) as context:
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=self.test_quantity,
                side="invalid_side",
                price=self.test_price
            )

        self.assertTrue("Invalid order side" in str(context.exception))
        self.mock_order_manager.add_order.assert_not_called()
        self.mock_alpaca_manager.place_market_order.assert_not_called()

    def test_zero_quantity(self):
        """Test handling of zero quantity orders"""
        with self.assertRaises(ValueError) as context:
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=0,
                side=self.test_side,
                price=self.test_price
            )

        self.assertTrue("Invalid quantity" in str(context.exception))
        self.mock_order_manager.add_order.assert_not_called()
        self.mock_alpaca_manager.place_market_order.assert_not_called()

    def test_negative_price(self):
        """Test handling of negative price orders"""
        with self.assertRaises(ValueError) as context:
            self.bridge.place_order(
                ticker_id=self.test_ticker_id,
                symbol=self.test_symbol,
                quantity=self.test_quantity,
                side=self.test_side,
                price=-1.0
            )

        self.assertTrue("Invalid price" in str(context.exception))
        self.mock_order_manager.add_order.assert_not_called()
        self.mock_alpaca_manager.place_market_order.assert_not_called()

    def test_update_order_status_filled(self):
        """Test updating an order to 'filled' status"""
        # Setup mock order status response
        self.mock_alpaca_manager.get_order_status.return_value = {
            "status": "filled",
            "filled_qty": 100.0,
            "avg_fill_price": 150.00
        }

        # Create mock order
        mock_order = Mock()
        mock_order.order_number = 1
        mock_order.filled_quantity = 0
        mock_order.add_fill = Mock()

        # Setup mock order manager
        self.mock_order_manager.orders = [mock_order]

        # Update order status
        self.bridge.update_order_status("1")

        # Verify interactions
        self.mock_alpaca_manager.get_order_status.assert_called_once_with("1")
        mock_order.add_fill.assert_called_once_with(
            price=150.00,
            quantity=100.0
        )

    def test_update_order_status_partially_filled(self):
        """Test updating an order to 'partially_filled' status"""
        # Setup mock order status response
        self.mock_alpaca_manager.get_order_status.return_value = {
            "status": "partially_filled",
            "filled_qty": 50.0,
            "avg_fill_price": 150.00
        }

        # Create mock order
        mock_order = Mock()
        mock_order.order_number = 1
        mock_order.filled_quantity = 0
        mock_order.add_fill = Mock()

        # Setup mock order manager
        self.mock_order_manager.orders = [mock_order]

        # Update order status
        self.bridge.update_order_status("1")

        # Verify interactions
        self.mock_alpaca_manager.get_order_status.assert_called_once_with("1")
        mock_order.add_fill.assert_called_once_with(
            price=150.00,
            quantity=50.0
        )

    def test_update_order_status_no_matching_order(self):
        """Test updating status when no matching order is found"""
        # Setup mock order status response
        self.mock_alpaca_manager.get_order_status.return_value = {
            "status": "filled",
            "filled_qty": 100.0,
            "avg_fill_price": 150.00
        }

        # Setup empty orders list
        self.mock_order_manager.orders = []

        # Update order status
        self.bridge.update_order_status("1")

        # Verify get_order_status was called but no fill was added
        self.mock_alpaca_manager.get_order_status.assert_called_once_with("1")

    def test_update_order_status_api_error(self):
        """Test handling of API error during status update"""
        # Setup mock to raise exception
        self.mock_alpaca_manager.get_order_status.side_effect = Exception("API Error")

        # Create mock order
        mock_order = Mock()
        mock_order.order_number = 1
        mock_order.filled_quantity = 0
        mock_order.add_fill = Mock()

        # Setup mock order manager
        self.mock_order_manager.orders = [mock_order]

        # Verify exception is raised
        with self.assertRaises(Exception) as context:
            self.bridge.update_order_status("1")

        self.assertTrue("API Error" in str(context.exception))
        mock_order.add_fill.assert_not_called()

if __name__ == '__main__':
    unittest.main()