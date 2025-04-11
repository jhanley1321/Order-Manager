# tests/test_alpaca_manager.py
import unittest
from unittest.mock import Mock, patch
from trading_platforms.alpaca_manager import AlpacaManager, AlpacaConfig

class TestAlpacaManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config = AlpacaConfig(
            api_key="test_key",
            secret_key="test_secret",
            paper_trading=True
        )

    @patch('trading_platforms.alpaca_manager.TradingClient')
    def test_market_order_creation(self, mock_trading_client):
        # Setup mock
        mock_order = Mock()
        mock_order.id = "test_order_id"
        mock_trading_client.return_value.submit_order.return_value = mock_order

        # Create manager and place order
        manager = AlpacaManager(self.config)
        order_id = manager.place_market_order("AAPL", 100, "buy")

        # Verify order was placed correctly
        self.assertEqual(order_id, "test_order_id")
        mock_trading_client.return_value.submit_order.assert_called_once()

    def test_invalid_side(self):
        """Test that invalid order sides are rejected"""
        manager = AlpacaManager(self.config)
        with self.assertRaises(ValueError):
            manager.place_market_order("AAPL", 100, "invalid_side")

if __name__ == '__main__':
    unittest.main()