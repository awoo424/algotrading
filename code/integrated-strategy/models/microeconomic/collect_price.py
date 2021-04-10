import pandas as pd
import yfinance as yf
import datetime, time   
import os

# get price data   
def get_price(ticker):
    
    # get price data from yfinance module
    hkex_data = yf.Ticker(ticker + '.HK')
    price_df = hkex_data.history(period='1')

    # data pre-processing
    price_df = price_df[~price_df.index.duplicated(keep='first')]
    price_df = price_df.reset_index()

    # set directory for saving results
    dir_name = os.getcwd() + '/database/daily_trading_data/data-results'
    result_path = os.path.join(dir_name, ticker.zfill(4) + '-result.csv') 

    df = pd.read_csv(result_path)
    # add closing price to df
    df['close'] = price_df['Close']

    df.to_csv(result_path,index=False)

    return df