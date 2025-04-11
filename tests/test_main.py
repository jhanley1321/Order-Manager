# tests/test_main.py
import unittest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
import os
from main import (
    initialize_alpaca_manager,
    main,
    run
)

class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock managers
        self.mock_order_manager = Mock()
        self.mock_alpaca_manager = Mock()

    @patch.dict(os.environ, {
        'ALPACA_MARKETS_API_KEY_TEST': 'test_key',
        'ALPACA_MARKETS_SECRET_KEY_TEST': 'test_secret'
    })
    @patch('main.AlpacaManager')
    def test_initialize_alpaca_manager_success(self, mock_alpaca_manager_class):
        """Test successful initialization of Alpaca manager"""
        # Setup mock
        mock_alpaca_manager_class.return_value = self.mock_alpaca_manager

        # Call function
        alpaca_manager = initialize_alpaca_manager()

        # Verify manager was created
        self.assertEqual(alpaca_manager, self.mock_alpaca_manager)
        mock_alpaca_manager_class.assert_called_once()

    @patch.dict(os.environ, {
        'ALPACA_MARKETS_API_KEY_TEST': '',
        'ALPACA_MARKETS_SECRET_KEY_TEST': ''
    })
    def test_initialize_alpaca_manager_missing_keys(self):
        """Test initialization with missing API keys"""
        with self.assertRaises(ValueError) as context:
            initialize_alpaca_manager()
        self.assertTrue("API keys not found" in str(context.exception))

class TestMainAsyncFunctions(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Set up test fixtures before each test method."""
        self.mock_order_manager = Mock()
        self.mock_alpaca_manager = Mock()
        self.mock_trading_bridge = Mock()

    @patch('main.OrderManager')
    @patch('main.initialize_alpaca_manager')
    @patch('main.TradingBridge')
    async def test_main_success(
        self,
        mock_trading_bridge_class,
        mock_initialize_alpaca,
        mock_order_manager_class
    ):
        """Test main function success path"""
        # Setup mocks
        mock_order_manager_class.return_value = self.mock_order_manager
        mock_initialize_alpaca.return_value = self.mock_alpaca_manager
        mock_trading_bridge_class.return_value = self.mock_trading_bridge

        # Setup mock return value for place_order
        self.mock_trading_bridge.place_order.return_value = "test_order_id"

        # Run main
        await main()

        # Verify components were initialized
        mock_order_manager_class.assert_called_once()
        mock_initialize_alpaca.assert_called_once()
        mock_trading_bridge_class.assert_called_once()

        # Verify order was placed
        self.mock_trading_bridge.place_order.assert_called_once()

        # Verify orders were saved
        self.mock_order_manager.save_orders.assert_called_once()

    @patch('main.OrderManager')
    @patch('main.initialize_alpaca_manager')
    async def test_main_initialization_error(self, mock_initialize_alpaca, mock_order_manager_class):
        """Test main function with initialization error"""
        # Setup mocks
        mock_order_manager_class.return_value = self.mock_order_manager
        mock_initialize_alpaca.side_effect = Exception("Init error")

        # Run main
        await main()

        # Verify cleanup was performed
        self.mock_order_manager.save_orders.assert_called_once()

class TestRunFunction(unittest.TestCase):
    @patch('asyncio.run')
    def test_run_success(self, mock_asyncio_run):
        """Test successful run"""
        run()
        mock_asyncio_run.assert_called_once()

    @patch('asyncio.run')
    def test_run_keyboard_interrupt(self, mock_asyncio_run):
        """Test run with keyboard interrupt"""
        mock_asyncio_run.side_effect = KeyboardInterrupt()
        run()  # Should not raise exception

    @patch('asyncio.run')
    def test_run_error(self, mock_asyncio_run):
        """Test run with error"""
        mock_asyncio_run.side_effect = Exception("Test error")
        run()  # Should not raise exception

if __name__ == '__main__':
    unittest.main()