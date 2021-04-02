import csv
import datetime, time
import os
import sys
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from models.sentiment.sentiment_vader import starter_vader
from models.sentiment.sentiment_text_blob import starter_textblob
from models.sentiment.collect_news_aastock import get_news_aastock


dir_name= os.getcwd()+'/database_daily/'
nltk.downloader.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()



def collect_news (ticker,days):
    
    news_report_postfix_url='/0/research-report'
    news_result_postfix_url='/0/result-announcement'
    news_daily_postfix_url='/0/hk-stock-news'
    news_indus_postfix_url='/0/industry-news'
    
    get_news_aastock(ticker,news_daily_postfix_url,'news-daily',days)
    get_news_aastock(ticker,news_report_postfix_url,'news-report',days)
    get_news_aastock(ticker,news_result_postfix_url,'news-result',days)
    get_news_aastock(ticker,news_indus_postfix_url,'news-indus',days)


# collect individual sentiment label for tickers in hkex    
def collect_individual_sentiment(ticker):
    try:
        print(ticker)
        path = os.path.join(dir_name,'data-news/data-aastock/'+'data-'+ticker.zfill(4)+'-aastock.csv') 
        result_path = os.path.join(dir_name,'data-results/'+'sentiment-'+ticker.zfill(4)+'-result.csv')
        vader_df=starter_vader(path,result_path)  
        text_blob_df=starter_textblob(path,result_path)  
        print(text_blob_df)
    except Exception as e:
        print(e)
        pass

    
def main():

    collect_news('0001',3)

    collect_individual_sentiment('0001')


if __name__ == "__main__":
    main() 