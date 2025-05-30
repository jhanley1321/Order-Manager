# tests/test_order_manager.py
import unittest
from order_manager import OrderManager, OrderDetails, OrderStatus
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
        details = OrderDetails(
            ticker_id=1001,
            order_quantity=100,
            order_price=50.00
        )
        order = self.manager.add_order(details)

        self.assertEqual(order.ticker_id, 1001)
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.order_price, 50.00)
        self.assertEqual(order.status, OrderStatus.OPEN)
        self.assertTrue(order.needs_fills)

    def test_order_filling(self):
        """Test filling an order"""
        details = OrderDetails(
            ticker_id=1001,
            order_quantity=100,
            order_price=50.00
        )
        order = self.manager.add_order(details)

        # Add partial fill
        self.manager.fill_order(1, 49.95, 60)
        self.assertEqual(order.status, OrderStatus.PARTIALLY_FILLED)
        self.assertEqual(order.filled_quantity, 60)
        self.assertEqual(order.remaining_quantity, 40)

        # Complete the order
        self.manager.fill_order(1, 50.05, 40)
        self.assertEqual(order.status, OrderStatus.FILLED)
        self.assertEqual(order.filled_quantity, 100)
        self.assertEqual(order.remaining_quantity, 0)
        self.assertFalse(order.needs_fills)

    def test_average_fill_price(self):
        """Test calculation of average fill price"""
        details = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(details)

        self.manager.fill_order(1, 49.00, 60)  # 2940
        self.manager.fill_order(1, 51.00, 40)  # 2040
        # Total cost: 4980 for 100 shares = 49.80 average

        self.assertEqual(order.average_fill_price, 49.80)

    def test_overfill_prevention(self):
        """Test that orders cannot be overfilled"""
        details = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(details)

        with self.assertRaises(ValueError):
            self.manager.fill_order(1, 50.00, 101)

    def test_fill_completed_order(self):
        """Test attempting to fill a completed order"""
        details = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(details)

        # Complete the order
        self.manager.fill_order(1, 50.00, 100)

        # Try to add another fill
        self.manager.fill_order(1, 51.00, 10)

        # Verify the order wasn't modified
        self.assertEqual(order.filled_quantity, 100)
        self.assertEqual(order.status, OrderStatus.FILLED)

    def test_get_open_orders(self):
        """Test retrieving open orders"""
        # Add two orders
        details1 = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.00)
        details2 = OrderDetails(ticker_id=1002, order_quantity=200, order_price=75.00)

        order1 = self.manager.add_order(details1)
        order2 = self.manager.add_order(details2)

        # Complete first order
        self.manager.fill_order(1, 50.00, 100)

        # Check open orders
        open_orders = self.manager.get_open_orders()
        self.assertEqual(len(open_orders), 1)
        self.assertEqual(open_orders[0], order2)

    def test_order_persistence(self):
        """Test saving and loading orders"""
        details = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.00)
        order = self.manager.add_order(details)

        self.manager.fill_order(1, 49.95, 60)
        self.manager.save_orders("test_orders.json")

        # Verify file exists and contains correct data
        file_path = os.path.join(self.test_data_folder, "test_orders.json")
        self.assertTrue(os.path.exists(file_path))

        

if __name__ == '__main__':
    unittest.main()