import streamlit as st
import pandas as pd
from typing import Optional
from order_manager import OrderManager, OrderDetails

class OrderManagerFrontend:
    """Frontend wrapper for OrderManager with Streamlit-specific logic"""
    
    def __init__(self, data_folder: str = "Data"):
        self.data_folder = data_folder
        self.manager = OrderManager(data_folder=data_folder)
    
    def _prepare_dataframe_for_display(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts fills column to display-friendly format"""
        if df.empty or 'fills' not in df.columns:
            return df
        
        display_df = df.copy()
        display_df['fills'] = display_df['fills'].apply(
            lambda x: f"{len(x)} fills" if isinstance(x, list) and len(x) > 0 else "No fills"
        )
        return display_df
    
    def display_all_orders(self):
        """Display all orders section"""
        st.header("All Orders")
        orders_df = self.manager.get_orders_as_dataframe()
        
        if not orders_df.empty:
            display_df = self._prepare_dataframe_for_display(orders_df)
            st.dataframe(display_df)
        else:
            st.info("No orders found.")
        
        return orders_df
    
    def display_orders_needing_fills(self, orders_df: pd.DataFrame):
        """Display orders that need fills section"""
        st.header("Orders that Need to be Filled")
        
        if not orders_df.empty and 'status' in orders_df.columns:
            needs_fills_df = orders_df[orders_df['status'].isin(['Open', 'Partially Filled'])]
            if not needs_fills_df.empty:
                display_df = self._prepare_dataframe_for_display(needs_fills_df)
                st.dataframe(display_df)
            else:
                st.info("No orders need fills.")
        else:
            st.info("No orders need fills.")
    
    def display_filled_orders(self, orders_df: pd.DataFrame):
        """Display filled orders section"""
        st.header("Orders that Have Been Filled")
        
        if not orders_df.empty and 'status' in orders_df.columns:
            filled_orders_df = orders_df[orders_df['status'] == 'Filled']
            if not filled_orders_df.empty:
                display_df = self._prepare_dataframe_for_display(filled_orders_df)
                st.dataframe(display_df)
            else:
                st.info("No filled orders.")
        else:
            st.info("No filled orders.")
    
    def add_order_section(self):
        """Add order input section"""
        st.header("Add Order")
        
        ticker_id = st.number_input("Ticker ID", min_value=0, step=1)
        order_quantity = st.number_input("Order Quantity", min_value=0.0, step=1.0)
        order_price = st.number_input("Order Price", min_value=0.0, step=0.01)
        exchange_id = st.number_input("Exchange ID", min_value=0, step=1)
        
        if st.button("Add Order"):
            return self._handle_add_order(ticker_id, order_quantity, order_price, exchange_id)
        
        return False
    
    def _handle_add_order(self, ticker_id: int, order_quantity: float, 
                         order_price: float, exchange_id: int) -> bool:
        """Handle adding a new order"""
        try:
            order_details = OrderDetails(
                ticker_id=ticker_id,
                order_quantity=order_quantity,
                order_price=order_price,
                exchange_id=exchange_id
            )
            
            # Add order to memory and append to file
            new_order = self.manager.add_order(order_details)
            self.manager.append_order(new_order, "orders.json")
            
            # Reload orders to keep memory in sync with file
            self.manager.load_orders("orders.json")
            
            st.success("Order added successfully!")
            return True
            
        except Exception as e:
            st.error(f"Error adding order: {str(e)}")
            return False
    
    def fill_order_section(self):
        """Fill order input section"""
        st.header("Fill Order")
        
        order_number = st.number_input("Order Number", min_value=1, step=1)
        fill_price = st.number_input("Fill Price", min_value=0.0, step=0.01)
        fill_quantity = st.number_input("Fill Quantity", min_value=0.0, step=1.0)
        
        if st.button("Fill Order"):
            return self._handle_fill_order(order_number, fill_price, fill_quantity)
        
        return False
    
    def _handle_fill_order(self, order_number: int, fill_price: float, 
                          fill_quantity: float) -> bool:
        """Handle filling an order"""
        try:
            # Fill order in memory and save all orders (overwrite file)
            self.manager.fill_order(order_number=order_number, 
                                  fill_price=fill_price, 
                                  fill_quantity=fill_quantity)
            self.manager.save_orders("orders.json")
            
            st.success("Order filled successfully!")
            return True
            
        except ValueError as e:
            st.error(str(e))
            return False
        except Exception as e:
            st.error(f"Error filling order: {str(e)}")
            return False
    
    def simulate_fills_section(self):
        """Simulate random fills section"""
        st.header("Simulate Random Fills")
        
        order_number = st.number_input("Order Number for Random Fills", min_value=1, step=1)
        use_custom_range = st.checkbox("Use custom price range")
        fill_price_range = None
        
        if use_custom_range:
            fill_price_range = st.slider("Fill Price Range", 
                                       min_value=0.0, max_value=200.0, 
                                       value=(90.0, 110.0), step=0.01)
        
        if st.button("Simulate Random Fills"):
            return self._handle_simulate_fills(order_number, fill_price_range)
        
        return False
    
    def _handle_simulate_fills(self, order_number: int, 
                              fill_price_range: Optional[tuple]) -> bool:
        """Handle simulating random fills"""
        try:
            # Simulate fills in memory and save all orders (overwrite file)
            self.manager.simulate_random_fills(order_number=order_number, 
                                             fill_price_range=fill_price_range)
            self.manager.save_orders("orders.json")
            
            st.success("Random fills simulated successfully!")
            return True
            
        except ValueError as e:
            st.error(str(e))
            return False
        except Exception as e:
            st.error(f"Error simulating fills: {str(e)}")
            return False
    
    def admin_section(self):
        """Admin functions section"""
        st.header("Admin Functions")
        col1, col2 = st.columns(2)
        
        actions_taken = []
        
        with col1:
            if st.button("Clear Orders from Memory"):
                self.manager.clear_orders()
                st.success("Orders cleared from memory!")
                actions_taken.append("clear")
        
        with col2:
            if st.button("Reload Orders from File"):
                self.manager.load_orders("orders.json")
                st.success("Orders reloaded from file!")
                actions_taken.append("reload")
        
        return actions_taken
    
    def run_app(self):
        """Main app runner"""
        st.title("Order Manager")
        
        # Display sections
        orders_df = self.display_all_orders()
        self.display_orders_needing_fills(orders_df)
        self.display_filled_orders(orders_df)
        
        # Action sections
        order_added = self.add_order_section()
        order_filled = self.fill_order_section()
        fills_simulated = self.simulate_fills_section()
        admin_actions = self.admin_section()
        
        # Rerun if any action was taken
        if order_added or order_filled or fills_simulated or admin_actions:
            st.rerun()