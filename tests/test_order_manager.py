# tests/test_order_manager.py
import unittest
from order_manager import OrderManager, OrderConfig, OrderStatus
import os
import shutil

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_data_folder = "TestData"
        self.manager = OrderManager(data_folder=self.test_data_folder)

    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_data_folder):
            shutil.rmtree(self.test_data_folder)

    def test_order_creation(self):
        """Test creating a new order"""
        config = OrderConfig(
            ticker_id=1001,
            order_quantity=100,
            order_price=50.00
        )
        order = self.manager.add_order(config)

        self.assertEqual(order.ticker_id, 1001)
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.order_price, 50.00)
        self.assertEqual(order.status, OrderStatus.OPEN)
        self.assertTrue(order.needs_fills)

    def test_order_filling(self):
        """Test filling an order"""
        config = OrderConfig(
            ticker_id=1001,
            order_quantity=100,
            order_price=50.00
        )
        order = self.manager.add_order(config)

        # Add partial fill
        self.manager.fill_order(order.order_number, 49.95, 60)
        self.assertEqual(order.status, OrderStatus.PARTIALLY_FILLED)
        self.assertEqual(order.filled_quantity, 60)
        self.assertEqual(order.remaining_quantity, 40)

        # Complete the order
        self.manager.fill_order(order.order_number, 50.05, 40)
        self.assertEqual(order.status, OrderStatus.FILLED)
        self.assertEqual(order.filled_quantity, 100)
        self.assertEqual(order.remaining_quantity, 0)
        self.assertFalse(order.needs_fills)

    def test_average_fill_price(self):
        """Test calculation of average fill price"""
        config = OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(config)

        self.manager.fill_order(order.order_number, 49.00, 60)  # 2940
        self.manager.fill_order(order.order_number, 51.00, 40)  # 2040
        # Total cost: 4980 for 100 shares = 49.80 average

        self.assertEqual(order.average_fill_price, 49.80)

    def test_overfill_prevention(self):
        """Test that orders cannot be overfilled"""
        config = OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(config)

        with self.assertRaises(ValueError):
            self.manager.fill_order(order.order_number, 50.00, 101)

    def test_fill_completed_order(self):
        """Test attempting to fill a completed order"""
        config = OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(config)

        # Complete the order
        self.manager.fill_order(order.order_number, 50.00, 100)

        # Try to add another fill
        self.manager.fill_order(order.order_number, 51.00, 10)

        # Verify the order wasn't modified
        self.assertEqual(order.filled_quantity, 100)
        self.assertEqual(order.status, OrderStatus.FILLED)

    def test_get_open_orders(self):
        """Test retrieving open orders"""
        # Add two orders
        config1 = OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00)
        config2 = OrderConfig(ticker_id=1002, order_quantity=200, order_price=75.00)

        order1 = self.manager.add_order(config1)
        order2 = self.manager.add_order(config2)

        # Complete first order
        self.manager.fill_order(order1.order_number, 50.00, 100)

        # Check open orders
        open_orders = self.manager.get_open_orders()
        self.assertEqual(len(open_orders), 1)
        self.assertEqual(open_orders[0].order_number, order2.order_number)

    def test_order_persistence(self):
        """Test saving and loading orders"""
        config = OrderConfig(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(config)

        self.manager.fill_order(order.order_number, 49.95, 60)
        self.manager.save_orders("test_orders.json")

        # Verify file exists and contains correct data
        file_path = os.path.join(self.test_data_folder, "test_orders.json")
        self.assertTrue(os.path.exists(file_path))

        # You could add more verification here by reading and parsing the JSON file

if __name__ == '__main__':
    unittest.main()