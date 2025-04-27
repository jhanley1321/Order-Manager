# c:\Data_Tools\Order_Manager\alpaca.py
import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus

# class AlpacaClient:
#     def __init__(self, is_paper=True):
#         """
#         Initialize the AlpacaClient with API credentials from environment variables.
        
#         :param is_paper: Boolean indicating whether to use the paper (True) or live (False) account.
#         """
#         self.is_paper = is_paper
#         self.api_key = os.getenv('ALPACA_MARKETS_API_KEY_TEST')
#         self.secret_key = os.getenv('ALPACA_MARKETS_SECRET_KEY_TEST')
        
#         self.api = TradingClient(self.api_key, self.secret_key, paper=is_paper)

#     def get_order_history(self):
#         """
#         Return the order history from the Alpaca API.
        
#         :return: List of order history
#         """
#         # Create a request to get all orders
#         request_params = GetOrdersRequest(
#             status=OrderStatus.ALL
#         )
        
#         # Fetch the orders
#         orders = self.api.get_orders(filter=request_params)
#         return orders



# def main():
#     client = AlpacaClient(is_paper=True)
#     order_history = client.get_order_history()
#     print(order_history)

# if __name__ == "__main__":
#     main()