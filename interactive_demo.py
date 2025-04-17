# interactive_demo.py
import os
import time
import random
from order_manager import OrderManager, OrderConfig, OrderStatus

def load_ticker_table(file_path: str) -> dict:
    """
    Load the ticker table from CSV into a dictionary mapping

    Args:
        file_path: Path to ticker table CSV file

    Returns:
        Dictionary containing ticker mappings
    """
    ticker_maps = {
        "tickers": {},      # ticker symbol -> id
        "names": {},        # asset name -> id
        "ticker_types": {}, # ticker type -> id
        "exchanges": {},    # exchange name -> id
        "exchange_ids": {}  # exchange id -> ticker id
    }

    if not os.path.exists(file_path):
        print(f"Warning: Ticker table not found at {file_path}")
        return ticker_maps

    try:
        with open(file_path, 'r') as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) != 6:
                    continue

                ticker_id = int(fields[0])
                ticker = fields[1].upper()
                name = fields[2].upper()
                ticker_type = fields[3].upper()
                exchange = fields[4].upper()
                exchange_id = int(fields[5])

                ticker_maps["tickers"][ticker] = ticker_id
                ticker_maps["names"][name] = ticker_id
                ticker_maps["ticker_types"][ticker_type] = ticker_id
                ticker_maps["exchanges"][exchange] = ticker_id
                ticker_maps["exchange_ids"][exchange_id] = ticker_id

        print(f"Loaded {len(ticker_maps['tickers'])} tickers")
        return ticker_maps
    except Exception as e:
        print(f"Error loading ticker table: {e}")
        return ticker_maps

def get_ticker_id(input_str: str, ticker_maps: dict) -> int:
    """Get ticker ID from ticker symbol"""
    input_str = input_str.upper()
    return ticker_maps["tickers"].get(input_str)

def get_exchange_id(input_str: str, ticker_maps: dict) -> int:
    """Get exchange ID from exchange name"""
    input_str = input_str.upper()
    return ticker_maps["exchanges"].get(input_str)

def lookup_ticker_id(input_str: str, ticker_maps: dict) -> int:
    """
    Look up ticker ID from ticker symbol, exchange name or asset name

    Args:
        input_str: Input string to look up
        ticker_maps: Dictionary of ticker mappings

    Returns:
        Ticker ID if found, None otherwise
    """
    input_str = input_str.upper()

    # Try ticker symbol first
    if input_str in ticker_maps["tickers"]:
        return ticker_maps["tickers"][input_str]

    # Try exchange name
    if input_str in ticker_maps["exchanges"]:
        return ticker_maps["exchanges"][input_str]

    # Try asset name
    if input_str in ticker_maps["names"]:
        return ticker_maps["names"][input_str]

    return None

def simulate_order_fills(manager, order, max_seconds=30):
    """
    Simulate filling an order with random fills and timing

    Args:
    manager: OrderManager instance
    order: Order to fill
    max_seconds: Maximum seconds to spend filling the order
    """
    print(f"\nSimulating fills for Order #{manager.orders.index(order) + 1}...")
    print(f"Total quantity to fill: {order.remaining_quantity}")
    print(f"Maximum simulation time: {max_seconds} seconds")

    start_time = time.time()
    remaining_time = max_seconds

    while order.needs_fills and remaining_time > 0:
        # Calculate a random delay for the next fill
        delay = min(random.uniform(0.5, 3.0), remaining_time)

        # Wait for the specified delay
        time.sleep(delay)

        # Calculate how much time remains
        elapsed = time.time() - start_time
        remaining_time = max_seconds - elapsed

        if remaining_time <= 0:
            print("Time limit reached!")
            break

        # Calculate random fill amount (between 5% and 40% of remaining)
        max_fill = min(order.remaining_quantity * 0.4, order.remaining_quantity)
        min_fill = min(order.remaining_quantity * 0.05, order.remaining_quantity)
        fill_qty = round(random.uniform(min_fill, max_fill), 2)

        # Calculate random price variation (±2% of order price)
        price_variation = order.order_price * 0.02
        fill_price = round(random.uniform(
            order.order_price - price_variation,
            order.order_price + price_variation
        ), 2)

        # Add the fill
        manager.fill_order(manager.orders.index(order) + 1, fill_price, fill_qty)

        # Print status update
        elapsed = time.time() - start_time
        print(f"[{elapsed:.1f}s] Filled {fill_qty} shares @ ${fill_price:.2f} " +
              f"({order.filled_quantity}/{order.quantity} total)")

    # Final status
    if order.is_filled:
        print(f"\nOrder #{manager.orders.index(order) + 1} completely filled in {time.time() - start_time:.1f} seconds")
        print(f"Average fill price: ${order.average_fill_price:.2f}")
    else:
        print(f"\nSimulation ended. Order #{manager.orders.index(order) + 1} is {order.filled_quantity}/{order.quantity} filled")
        print(f"Remaining to fill: {order.remaining_quantity}")

    # Save the order after simulation
    manager.save_orders()
    print("Order fills saved to disk")

def run_interactive_demo():
    """Interactive version of the order manager demo"""
    # Create an order manager
    manager = OrderManager()

    # Load ticker information
    ticker_maps = load_ticker_table(manager.data_folder)

    # Try to load previously saved orders
    manager.load_orders()

    while True:
        print("\nOrder Manager Menu:")
        print("1. List all orders")
        print("2. Add new order")
        print("3. Fill an existing order")
        print("4. Show open orders")
        print("5. Simulate automatic fills")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            print("\nList of all orders:")
            manager.list_orders()

        elif choice == '2':
            try:
                # Show available tickers
                print("\nAvailable tickers:")
                print("Symbol\tName\t\tType")
                print("----\t----\t\t----")

                # If we have the ticker_table.csv loaded, display available options
                if ticker_maps["tickers"]:
                    for ticker, ticker_id in ticker_maps["tickers"].items():
                        # Find corresponding asset name
                        asset_name = "Unknown"
                        ticker_type = "Unknown"
                        for name, id in ticker_maps["names"].items():
                            if id == ticker_id:
                                asset_name = name.title()
                                break
                        print(f"{ticker}\t{asset_name}\t{ticker_type}")
                else:
                    print("No ticker information available. You'll need to enter ticker IDs manually.")

                # Get ticker input
                ticker_input = input("\nEnter ticker symbol or asset name: ")
                ticker_id = lookup_ticker_id(ticker_input, ticker_maps)

                if ticker_id is None:
                    try:
                        # If lookup failed, try to parse as a direct ticker ID
                        ticker_id = int(ticker_input)
                        print(f"Using ticker ID: {ticker_id}")
                    except ValueError:
                        print(f"Unknown ticker: {ticker_input}")
                        continue
                else:
                    print(f"Found ticker ID: {ticker_id}")

                quantity = float(input("Enter order quantity: "))
                price = float(input("Enter order price: "))

                config = OrderConfig(ticker_id=ticker_id, order_quantity=quantity, order_price=price)
                order = manager.add_order(config)

                print(f"\nCreated Order #{manager.orders.index(order) + 1}: {order.quantity} shares of ticker {order.ticker_id} @ ${order.order_price:.2f}")

                # Save orders after creating a new order
                manager.save_orders()
                print("Order saved to disk")
            except ValueError as e:
                print(f"Invalid input! Order creation cancelled: {e}")

        elif choice == '3':
            open_orders = manager.get_open_orders()

            if not open_orders:
                print("No open orders to fill!")
                continue

            # Display open orders
            print("\nOpen orders that can be filled:")
            for i, order in enumerate(open_orders):
                print(f"{i+1}. Order #{manager.orders.index(order) + 1}: {order.remaining_quantity} shares of ticker {order.ticker_id} remaining @ ${order.order_price:.2f}")

            # Allow user to select order to fill
            try:
                selection = int(input("\nSelect an order to fill (number): ")) - 1
                if 0 <= selection < len(open_orders):
                    order = open_orders[selection]

                    # Get fill details
                    try:
                        fill_price = float(input(f"Enter fill price (current price: ${order.order_price:.2f}): "))
                        max_fill = order.remaining_quantity
                        fill_qty = float(input(f"Enter fill quantity (max: {max_fill}): "))

                        if 0 < fill_qty <= max_fill:
                            manager.fill_order(manager.orders.index(order) + 1, fill_price, fill_qty)
                            print(f"Filled {fill_qty} shares of Order #{manager.orders.index(order) + 1} @ ${fill_price:.2f}")

                            # Save orders after filling an order
                            manager.save_orders()
                            print("Order fill saved to disk")
                        else:
                            print("Invalid fill quantity!")
                    except ValueError:
                        print("Invalid input! Fill operation cancelled.")
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Invalid input! No order filled.")

        elif choice == '4':
            open_orders = manager.get_open_orders()
            print(f"\nThere are {len(open_orders)} open orders remaining")
            for order in open_orders:
                print(f"Order #{manager.orders.index(order) + 1}: {order.remaining_quantity} shares of ticker {order.ticker_id} remaining @ ${order.order_price:.2f}")

        elif choice == '5':
            # Simulate automatic fills
            open_orders = manager.get_open_orders()

            if not open_orders:
                print("No open orders to simulate!")
                continue

            # Display open orders
            print("\nOpen orders that can be simulated:")
            for i, order in enumerate(open_orders):
                print(f"{i+1}. Order #{manager.orders.index(order) + 1}: {order.remaining_quantity} shares of ticker {order.ticker_id} remaining @ ${order.order_price:.2f}")

            # Allow user to select order to simulate
            try:
                selection = int(input("\nSelect an order to simulate (number): ")) - 1
                if 0 <= selection < len(open_orders):
                    order = open_orders[selection]

                    # Get simulation parameters
                    try:
                        max_seconds = int(input("Enter maximum simulation time in seconds (5-60): "))
                        if 5 <= max_seconds <= 60:
                            # Run the simulation
                            simulate_order_fills(manager, order, max_seconds)
                        else:
                            print("Invalid time! Must be between 5 and 60 seconds.")
                    except ValueError:
                        print("Invalid input! Simulation cancelled.")
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Invalid input! No simulation started.")

        elif choice == '6':
            # Final save before exiting
            manager.save_orders()
            print("\nAll orders saved to disk")
            print("Exiting Order Manager Demo")
            break

        else:
            print("Invalid choice! Please enter a number between 1-6.")

if __name__ == "__main__":
    run_interactive_demo()