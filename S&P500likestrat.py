import numpy as py
import pandas as pd
import requests
import xlsxwriter
import math


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


stocks = pd.read_csv('sp_500_stocks.csv')

from secret import IEX_CLOUD_API_TOKEN

symbol_groups = list(chunks(stocks['Ticker'],100))  #we are pulling from a fake list of f500 compagnies I have implemented with a real one
symbol_strings = []
for i in range ( 0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

my_columns = ['Ticker', 'Stock Price' , 'Market Capatalization', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'     # this is a sandbox version of the api I have used a real one in my personal implementation
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
        pd.Series(
        [
            symbol,
            data[symbol]['quote']['latestPrice'],
            data[symbol]['quote']['marketCap'],
            'N/A'
        ],
        index = my_columns),
        ignore_index=True
        )

portfolio_size = float(input('Enter value of portfolio')) #this is for practice and testing. In actual use this is linked to my auto trader to pull how much money is available. If you actually wanted to use this taking user input implement a try catch block to deal with user error
position_size = portfolio_size / len(final_dataframe.index)
for i in range (0,len(final_dataframe.index)):
    final_dataframe.loc[i,'Number of Shares to Buy'] = math.floor(position_size/ final_dataframe['Price'][i])
#the rest of the code here is exporting my buy data to a csv. In actuallity this would be fed to autotrader to execute the trades
writer = pd.ExcelWriter('S&P500 trade amounts' , engine = 'xlsxwriter') #file name and specify excel file
final_dataframe.to_excel(writer, 'Recommended Trades', index = False)
bg_color = '#0a0a23' #for excel customization
font_color = '#ffffff' #for excel customization
string_format = writer.book.add_format( {
    'font_color': font_color,
    'bg_color': bg_color,
    'border' : 1
})
