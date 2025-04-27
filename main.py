# c:\Data_Tools\Order_Manager\main.py
import json
import os
from datetime import datetime
from order_manager import OrderManager, OrderDetails, OrderStatus, Order, OrderFill
from front_end import run_order_manager_app




def main():
     # Create an instance of OrderManager
    manager = OrderManager(data_folder="Data")
   
    
    # set order details
    order1 = OrderDetails(ticker_id=1001, order_quantity=100, order_price=50.0, exchange_id=1)
    
    # load orders
    # manager.load_orders("orders.json") # may no longer be needed maybe
    
    
    # Place Orders
    manager.add_order(order1)
    

    
   
    # # Fill Orders
    manager.fill_order(order_number=1, fill_price=49.95, fill_quantity=60)
    manager.fill_order(order_number=1, fill_price=50.05, fill_quantity=40)
    
    # manager.fill_order(order_number=3, fill_price=50.05, fill_quantity=40)

     # Should only be needed for order back into memeory
    manager.save_orders("orders.json")


    # Append orders
    # manager.append_orders("orders.json")
   
   
   
   
    # manager.list_orders()
    
    # Display Order Options (pickone at a time)
    # manager.list_orders() # Displays
    print(manager.get_orders_as_dataframe())   # view as a dataframe







if __name__ == '__main__':
    main()
   