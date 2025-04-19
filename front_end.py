import streamlit as st
from order_manager import OrderManager, OrderDetails
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
        config = OrderDetails(
            ticker_id=ticker_id,
            order_quantity=order_quantity,
            order_price=order_price,
            exchange_id=exchange_id
        )
        manager.add_order(config)
        manager.save_orders("orders.json")  # Save the orders immediately after adding
        st.sidebar.success("Order added and saved successfully!")

    # Sidebar for filling orders
    st.sidebar.header("Fill an Order")
    # Get list of open orders that need fills
    open_orders = [order for order in manager.orders if order.needs_fills]
    if open_orders:
        order_options = [f"Order #{manager.orders.index(order) + 1} - Ticker {order.ticker_id}"
                        for order in open_orders]
        selected_order_idx = st.sidebar.selectbox("Select Order to Fill",
                                                range(len(order_options)),
                                                format_func=lambda x: order_options[x])

        fill_quantity = st.sidebar.number_input("Fill Quantity",
                                              min_value=0.0,
                                              max_value=open_orders[selected_order_idx].remaining_quantity,
                                              value=min(100.0, open_orders[selected_order_idx].remaining_quantity),
                                              step=1.0)

        fill_price = st.sidebar.number_input("Fill Price",
                                           min_value=0.0,
                                           value=open_orders[selected_order_idx].order_price,
                                           step=0.01)

        fill_order_button = st.sidebar.button("Fill Order")

        if fill_order_button:
            try:
                selected_order = open_orders[selected_order_idx]
                order_number = manager.orders.index(selected_order) + 1
                # Remove the keyword arguments and pass them positionally
                manager.fill_order(order_number, fill_price, fill_quantity)
                manager.save_orders("orders.json")  # Save after filling
                st.sidebar.success("Order filled successfully!")
            except Exception as e:
                st.sidebar.error(f"Error filling order: {str(e)}")
    else:
        st.sidebar.info("No orders available for filling")

    # Main content for listing orders
    st.header("Current Orders")
    df = manager.get_orders_as_dataframe()
    st.dataframe(df)





if __name__ == '__main__':
    run_order_manager_app()