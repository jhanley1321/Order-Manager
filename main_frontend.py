import streamlit as st
import json
import os
from order_manager import OrderManager, OrderDetails, OrderStatus, Order, OrderFill

# Initialize the OrderManager
manager = OrderManager(data_folder="Data")

# Streamlit app
st.title("Order Manager")

# Load and display orders by default
st.header("Current Orders")
orders_df = manager.get_orders_as_dataframe()
if not orders_df.empty:
    st.dataframe(orders_df)
else:
    st.info("No orders found.")

# Add Order
st.header("Add Order")
ticker_id = st.number_input("Ticker ID", min_value=0, step=1)
order_quantity = st.number_input("Order Quantity", min_value=0.0, step=1.0)
order_price = st.number_input("Order Price", min_value=0.0, step=0.01)
exchange_id = st.number_input("Exchange ID", min_value=0, step=1)

if st.button("Add Order"):
    order_details = OrderDetails(ticker_id=ticker_id, order_quantity=order_quantity, order_price=order_price, exchange_id=exchange_id)
    manager.add_order(order_details)
    manager.save_orders("orders.json")  # Save orders after adding
    st.success("Order added successfully!")
    st.rerun()  # Refresh the page to show the updated orders

# Fill Order
st.header("Fill Order")
order_number = st.number_input("Order Number", min_value=1, step=1)
fill_price = st.number_input("Fill Price", min_value=0.0, step=0.01)
fill_quantity = st.number_input("Fill Quantity", min_value=0.0, step=1.0)

if st.button("Fill Order"):
    try:
        manager.fill_order(order_number=order_number, fill_price=fill_price, fill_quantity=fill_quantity)
        manager.save_orders("orders.json")  # Save orders after filling
        st.success("Order filled successfully!")
        st.rerun()  # Refresh the page to show the updated orders
    except ValueError as e:
        st.error(str(e))

# Save Orders
# Removed explicit save button as orders are saved automatically