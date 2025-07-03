# c:\Data_Tools\Order_Manager\main.py
import json
import os
from datetime import datetime
from order_manager import OrderManager, OrderDetails, OrderStatus, Order, OrderFill
from frontend import OrderManagerFrontend





def sample_order1():
    # Create an instance of OrderManager
    manager = OrderManager(data_folder="data")
    
    # Set order details with transaction fee
    order1 = OrderDetails(
        ticker_id=0, 
        order_quantity=100, 
        order_price=50.0, 
        exchange_id=1, 
        transaction_fee=2.5  # Example transaction fee
    )
    

    order2 = OrderDetails(
        ticker_id=0, 
        order_quantity=1000, 
        order_price=60.0, 
        exchange_id=1, 
        transaction_fee=2.5  # Example transaction fee
    )

    order3 = OrderDetails(
        ticker_id=0, 
        order_quantity=2000, 
        order_price=70.0, 
        exchange_id=1, 
        transaction_fee=2.5  # Example transaction fee
    )
    
    order4 = OrderDetails(
        ticker_id=0, 
        order_quantity=90000, 
        order_price=70.0, 
        exchange_id=1, 
        transaction_fee=2.5  # Example transaction fee
    )


    # load orders test
    manager.load_orders()

    # Place Orders
    manager.add_order(order1)
    # # manager.save_orders("orders.json")
    manager.add_order(order2)
    # # manager.save_orders("orders.json")
    manager.add_order(order3)
    # manager.save_orders("orders.json")
    # manager.append_orders("orders.json")
    manager.add_order(order4)
    
    
    # Fill Orders
    manager.fill_order(order_number=1, fill_price=50, fill_quantity=70)
    manager.fill_order(order_number=1, fill_price=50, fill_quantity=30)
    manager.save_orders("orders.json")

    manager.fill_order(order_number=2, fill_price=60, fill_quantity=500)
    manager.fill_order(order_number=2, fill_price=60, fill_quantity=200)
    manager.fill_order(order_number=2, fill_price=60, fill_quantity=300)
    manager.save_orders("orders.json")

    manager.fill_order(order_number=3, fill_price=70, fill_quantity=200)
    manager.fill_order(order_number=3, fill_price=70, fill_quantity=200)
    manager.fill_order(order_number=3, fill_price=70, fill_quantity=200)
    manager.save_orders("orders.json")
    
    # Save orders to a JSON file
    # manager.save_orders("orders.json")
    # manager.append_orders("orders.json")

    # Display orders as a DataFrame
    print(manager.get_orders_as_dataframe())



def sample_order1_fill():
    # Create an instance of OrderManager
    manager = OrderManager(data_folder="data")
    
    
    manager.load_orders()
    
  

    

    manager.fill_order(order_number=1, fill_price=50, fill_quantity=70)
    



def main(run_front_end=True):
    if run_front_end:
        frontend = OrderManagerFrontend(data_folder="data")
        frontend.run_app()

    else:
        sample_order1()


if __name__ == '__main__':
    main()
   