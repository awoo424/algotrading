import pandas as pd
import yfinance as yf
import datetime, time   
import os
# get price data   
def get_price(ticker):
    
    hkex_data = yf.Ticker(ticker+'.HK')
    price_df = hkex_data.history(period='1')
    price_df = price_df[~price_df.index.duplicated(keep='first')]
    price_df=price_df.reset_index()

    dir_name= os.getcwd()+'/database_daily/data-results'
    sentiment_path= os.path.join(dir_name,ticker.zfill(4)+'-result.csv') 
    df=pd.read_csv(sentiment_path)

    df['close']=price_df['Close']


    df.to_csv(sentiment_path,index=False)
    return df