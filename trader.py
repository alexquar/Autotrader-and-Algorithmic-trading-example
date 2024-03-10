import pandas as pd
#connect to market
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails

#import api credentials from secret file
from secret import access_token, accountID


# Read stock amounts to buy from Excel file
def read_stock_amounts(file_path):
    try:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            stock_symbol = row['Ticker']
            amount_to_buy = row['Number of Shares to Buy']
            execute_trade(stock_symbol, amount_to_buy)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")

# Function to execute trades 
def execute_trade(stock_symbol, amount):
    #verify your account with broker
    #set up how you would like to make transactions here, scheduled/automatically on an event/manual/.....#
    pass

read_stock_amounts('excel file name') #get the excel file name from the code of whichever strat is being used
