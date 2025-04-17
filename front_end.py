
def run_order_manager_app():
    # Initialize the OrderManager
    data_folder = "Data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    manager = OrderManager(data_folder=data_folder)

    # Streamlit app
    st.title("Order Manager Front End")

    # Sidebar for adding new orders
    st.sidebar.header("Add New Order")
    ticker_id = st.sidebar.number_input("Ticker ID", min_value=1, value=1, step=1)
    order_quantity = st.sidebar.number_input("Order Quantity", min_value=0.0, value=100.0, step=1.0)
    order_price = st.sidebar.number_input("Order Price", min_value=0.0, value=50.0, step=0.01)
    exchange_id = st.sidebar.number_input("Exchange ID", min_value=1, value=1, step=1)
    add_order_button = st.sidebar.button("Add Order")

    if add_order_button:
        config = OrderConfig(
            ticker_id=ticker_id,
            order_quantity=order_quantity,
            order_price=order_price,
            exchange_id=exchange_id
        )
        manager.add_order(config)
        st.sidebar.success("Order added successfully!")

    # Main content for listing orders
    st.header("Current Orders")
    if manager.orders:
        # Create DataFrame for orders
        orders_data = []
        for order in manager.orders:
            order_data = {
                'Order #': manager.orders.index(order) + 1,
                'Ticker ID': order.ticker_id,
                'Exchange ID': order.exchange_id,
                'Original Quantity': order.quantity,
                'Order Price': order.order_price,
                'Created At': order.created_at,
                'Status': order.status.value,
                'Needs Fills': 'Yes' if order.needs_fills else 'No',
                'Filled Quantity': order.filled_quantity,
                'Remaining Quantity': order.remaining_quantity,
                'Average Fill Price': order.average_fill_price if order.fills else '-'
            }
            orders_data.append(order_data)

        df = pd.DataFrame(orders_data)
        st.dataframe(df)

        # Display fill history for each order
        for order in manager.orders:
            if order.fills:
                st.subheader(f"Fill History for Order #{manager.orders.index(order) + 1}")
                fills_data = []
                for fill in order.fills:
                    fills_data.append({
                        'Fill Quantity': fill.fill_quantity,
                        'Fill Price': fill.fill_price,
                        'Filled At': fill.filled_at
                    })
                fills_df = pd.DataFrame(fills_data)
                st.dataframe(fills_df)
    else:
        st.write("No orders found.")

    # Save and load orders
    st.sidebar.header("Save and Load Orders")
    save_orders_button = st.sidebar.button("Save Orders")
    load_orders_button = st.sidebar.button("Load Orders")

    if save_orders_button:
        manager.save_orders("orders.json")
        st.sidebar.success("Orders saved successfully!")

    if load_orders_button:
        manager.load_orders("orders.json")
        st.sidebar.success("Orders loaded successfully!")# order_manager_front_end.py
import streamlit as st
from order_manager import OrderManager, OrderConfig
import os
import pandas as pd

def run_order_manager_app():
    # Initialize the OrderManager
    data_folder = "Data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    manager = OrderManager(data_folder=data_folder)

    # Streamlit app
    st.title("Order Manager Front End")

    # Sidebar for adding new orders
    st.sidebar.header("Add New Order")
    ticker_id = st.sidebar.number_input("Ticker ID", min_value=1, value=1, step=1)
    order_quantity = st.sidebar.number_input("Order Quantity", min_value=0.0, value=100.0, step=1.0)
    order_price = st.sidebar.number_input("Order Price", min_value=0.0, value=50.0, step=0.01)
    exchange_id = st.sidebar.number_input("Exchange ID", min_value=1, value=1, step=1)
    add_order_button = st.sidebar.button("Add Order")

    if add_order_button:
        config = OrderConfig(
            ticker_id=ticker_id,
            order_quantity=order_quantity,
            order_price=order_price,
            exchange_id=exchange_id
        )
        manager.add_order(config)
        st.sidebar.success("Order added successfully!")

    # Main content for listing orders
    st.header("Current Orders")
    if manager.orders:
        # Create DataFrame for orders
        orders_data = []
        for order in manager.orders:
            order_data = {
                'Order #': manager.orders.index(order) + 1,
                'Ticker ID': order.ticker_id,
                'Exchange ID': order.exchange_id,
                'Original Quantity': order.quantity,
                'Order Price': order.order_price,
                'Created At': order.created_at,
                'Status': order.status.value,
                'Needs Fills': 'Yes' if order.needs_fills else 'No',
                'Filled Quantity': order.filled_quantity,
                'Remaining Quantity': order.remaining_quantity,
                'Average Fill Price': order.average_fill_price if order.fills else '-'
            }
            orders_data.append(order_data)

        df = pd.DataFrame(orders_data)
        st.dataframe(df)

        # Display fill history for each order
        for order in manager.orders:
            if order.fills:
                st.subheader(f"Fill History for Order #{manager.orders.index(order) + 1}")
                fills_data = []
                for fill in order.fills:
                    fills_data.append({
                        'Fill Quantity': fill.fill_quantity,
                        'Fill Price': fill.fill_price,
                        'Filled At': fill.filled_at
                    })
                fills_df = pd.DataFrame(fills_data)
                st.dataframe(fills_df)
    else:
        st.write("No orders found.")

    # Save and load orders
    st.sidebar.header("Save and Load Orders")
    save_orders_button = st.sidebar.button("Save Orders")
    load_orders_button = st.sidebar.button("Load Orders")

    if save_orders_button:
        manager.save_orders("orders.json")
        st.sidebar.success("Orders saved successfully!")

    if load_orders_button:
        manager.load_orders("orders.json")
        st.sidebar.success("Orders loaded successfully!")

