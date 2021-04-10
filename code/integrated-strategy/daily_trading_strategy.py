import csv
import datetime
import time
import os
import sys
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from models.sentiment.sentiment_vader import starter_vader
from models.sentiment.sentiment_text_blob import starter_textblob
from models.sentiment.collect_news_aastock import get_news_aastock
from models.microeconomic.collect_price import get_price
from models.LSTM import predict_price_daily
from utils import load_test_data, gen_signal_daily
from pandas.tseries.offsets import BDay
from datetime import date

import torch
import torch.nn as nn
from torch.autograd import Variable

# set directory with daily trading data
dir_name = os.getcwd() + '/database/daily_trading_data/'

# for VADER sentiment analysis
nltk.downloader.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()

# collect news data for ticker
def collect_news(ticker, days):

    news_report_postfix_url = '/0/research-report'
    news_result_postfix_url = '/0/result-announcement'
    news_daily_postfix_url = '/0/hk-stock-news'
    news_indus_postfix_url = '/0/industry-news'

    # get news data
    get_news_aastock(ticker, news_daily_postfix_url, 'news-daily', days)
    get_news_aastock(ticker, news_report_postfix_url, 'news-report', days)
    get_news_aastock(ticker, news_result_postfix_url, 'news-result', days)
    get_news_aastock(ticker, news_indus_postfix_url, 'news-indus', days)


# collect macreconomic data (gdp, u_rate, pprice) for ticker
def collect_macro_data(df, dir_name, ticker):

    path = os.path.join(dir_name, 'data-results/macro-data.csv')

    macro_data = pd.read_csv(path)
    macro_data = macro_data.iloc[-1]
    
    df['gdp'] = macro_data['gdp']
    df['Unemployment rate'] = macro_data['unemployment_rate_seasonally_adjusted']
    df['Property price'] = macro_data['average_price_per_sqft']

    res_path = os.path.join(dir_name, 'data-results/' +
                            ticker.zfill(4)+'-result.csv')

    df.to_csv(res_path, index=False)
    
    return df


# collect individual sentiment label for ticker in hkex
def collect_individual_sentiment(ticker):
    try:
        path = os.path.join(dir_name, 'data-news/' + 'data-' +
                            ticker.zfill(4) + '-aastock.csv')

        result_path = os.path.join(
            dir_name, 'data-results/' + ticker.zfill(4) + '-result.csv')

        vader_df = starter_vader(path, result_path)
        text_blob_df = starter_textblob(path, result_path)

    except Exception as e:
        print(e)
        pass


def main():
    # load directory for storing daily trading signals
    #dir_name = os.getcwd() + '/database/daily_trading_data/'

    # set ticker to trade
    ticker = '0001'
    result_path = os.path.join(dir_name, 'signal/' + ticker.zfill(4) + '-signal.csv')

    # collect news data
    collect_news(ticker, 3)
    collect_individual_sentiment('0001')
    
    # get price data
    df = get_price(ticker)

    # get macroeconomic data
    res_df = collect_macro_data(df, dir_name, ticker)
    res_df = res_df.set_index('dates')

    df, scaled, scaler = load_test_data(res_df)

    # load model
    model = torch.load('./saved_models/0001_model')

    # inferencing
    y_inf_pred = predict_price_daily(scaled, model, scaler)
    signal_dataframe = gen_signal_daily(y_inf_pred[:, 2], df.iloc[0, 2], df.index)
    signal_dataframe['pred_price'] = y_inf_pred[:, 2]

    # save signals as csv file
    signal_dataframe.to_csv(result_path, index=False)


if __name__ == "__main__":
    main()
