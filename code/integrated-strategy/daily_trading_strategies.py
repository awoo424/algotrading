import csv
import datetime, time
import os
import sys
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# mpl.use('tkagg')  # issues with Big Sur

from models.sentiment.sentiment_vader import starter_vader
from models.sentiment.sentiment_text_blob import starter_textblob
from models.sentiment.collect_news_aastock import get_news_aastock
from models.microeconomic.collect_price import get_price
from models.LSTM import predict_price_daily
from utils import load_test_data,gen_signal_daily
from pandas.tseries.offsets import BDay
from datetime import date
import torch
import torch.nn as nn
from torch.autograd import Variable



dir_name= os.getcwd()+'/database_daily/'
nltk.downloader.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()



def collect_news (ticker,days):
    
    news_report_postfix_url='/0/research-report'
    news_result_postfix_url='/0/result-announcement'
    news_daily_postfix_url='/0/hk-stock-news'
    news_indus_postfix_url='/0/industry-news'
    # get news data
    get_news_aastock(ticker,news_daily_postfix_url,'news-daily',days)
    get_news_aastock(ticker,news_report_postfix_url,'news-report',days)
    get_news_aastock(ticker,news_result_postfix_url,'news-result',days)
    get_news_aastock(ticker,news_indus_postfix_url,'news-indus',days)

def collect_macro_data(df,dir_name,ticker):
 

    path=os.path.join(dir_name,'data-results/macro-data.csv')

    macro_data=pd.read_csv(path)
    macro_data=macro_data.iloc[-1]
    # print(macro_data)
    df['gdp']=macro_data['gdp']
    df['Unemployment rate']=macro_data['unemployment_rate_seasonally_adjusted']
    df['Property price']=macro_data['average_price_per_sqft']
    
    
    res_path= os.path.join(dir_name,'data-results/'+ticker.zfill(4)+'-result.csv') 
    # df=df.set_index('dates')
    df.to_csv(res_path,index=False)
    # print(df)
    return df
 
   
   
    # return res
   
# collect individual sentiment label for tickers in hkex    
def collect_individual_sentiment(ticker):
    try:
        print(ticker)
        path = os.path.join(dir_name,'data-news/'+'data-'+ticker.zfill(4)+'-aastock.csv') 
        result_path = os.path.join(dir_name,'data-results/'+ticker.zfill(4)+'-result.csv')
        vader_df=starter_vader(path,result_path)  
        text_blob_df=starter_textblob(path,result_path)  
        print(text_blob_df)
    except Exception as e:
        print(e)
        pass



    
def main():
    dir_name= os.getcwd()+'/database_daily/'
    
    ticker='0001'
    result_path = os.path.join(dir_name,'signal/'+ticker.zfill(4)+'-signal.csv')
    # collect news data
    collect_news(ticker,3)
    collect_individual_sentiment('0001')
    # get price data
    # print('hello')
    df=get_price(ticker)
    # print(df)
    res_df=collect_macro_data(df,dir_name,ticker)
    # print(res_df)
    res_df=res_df.set_index('dates')
    # print(res_df)
    df, scaled, scaler=load_test_data(res_df)
    model = torch.load('0001_model')
    # print(scaled.shape)
    # Inferencing
    y_inf_pred = predict_price_daily(scaled, model, scaler)
    # print(y_inf_pred)
    # print(y_inf_pred[:,2])
    signal_dataframe = gen_signal_daily(y_inf_pred[:,2], df.iloc[0,2], df.index)


    signal_dataframe['pred_price']=y_inf_pred[:,2]
    print(signal_dataframe)
    signal_dataframe.to_csv(result_path,index=False)



if __name__ == "__main__":
    main() 