import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
import os

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import twitter_samples
from sklearn.model_selection import train_test_split

# directory to sentiment data
dir_name = '../../database_real/sentiment_data/'

# initialise sentiment analyser
analyser = SentimentIntensityAnalyzer()

# input: @signals, signals dataframe
# output: @filtered_signals, filtered signals dataframe


def SentimentFilter(ticker, signals):
    sentiment_scores = starter_vader(ticker)
    sentiment_scores['dates'] = pd.to_datetime(sentiment_scores['dates'])

    # check if sentiment label contrasting with buy/sell signals
    merged_df = signals.merge(sentiment_scores, how='left', left_on='Date', right_on='dates')
    #print(merged_df.head())

    # create new column for filtered signals
    merged_df['filtered_signal'] = merged_df['signal']

    buy_signal = (merged_df['signal'] == 1.0)
    sell_signal = (merged_df['signal'] == -1.0)
    pos_label = (merged_df['vader_label'] == 2)
    neg_label = (merged_df['vader_label'] == 0)

    # when there is a buy signal but a -ve label
    merged_df[(buy_signal) & (neg_label)]['filtered_signal'] = 0.0
    # when there is a sell signal but a +ve label
    merged_df[(sell_signal) & (pos_label)]['filtered_signal'] = 0.0

    # generate positions with filtered signals
    merged_df['filtered_positions'] = merged_df['filtered_signal'].diff()

    merged_df = merged_df.drop(['dates', 'compound_vader_score', 'hsi_average', 'signal', 'positions'], axis=1)
    #print(merged_df)
    
    filtered_signals = pd.merge(signals, merged_df, how="left", on="Date")
    filtered_signals = filtered_signals.drop(columns=['positions', 'signal'])
    filtered_signals = filtered_signals.set_index('Date')
    filtered_signals = filtered_signals[~filtered_signals.index.duplicated()] # remove duplicate rows
    #print(filtered_signals)
    filtered_signals = filtered_signals.rename({'filtered_positions': 'positions', 'vader_label': 'vader_label', 'filtered_signal': 'signal'}, axis=1)
    
    return filtered_signals


# output dataframe with vader sentiment label
def starter_vader(ticker_full):
    ticker = ticker_full[0:4]
    # get the full path of ticker
    path = os.path.join(dir_name, 'data-news/data-aastock/' +
                        'data-' + ticker.zfill(5) + '-aastock.csv')
    df = pd.read_csv(path, names=['dates', 'news'])
    # read append the compound vader score to the pandas dataframe
    df = read_news_path(df)
    # pass in the threshold to get the vader label
    df = find_news_pred_label(df, 0.01)

    result_path = 'sentiment_scores/' + ticker_full + '-sentiment-scores.csv'

    # get the full path of the hang seng index average csv file
    hsi_movement_path = os.path.join(
        dir_name, 'train-data/hkex/hsi_movement.csv')
    # merge the df pandas with the hsi_average
    df = merge_actual_label(df, hsi_movement_path)

    # store to csv file if the dataset is not empty
    if (df.empty == False):
        df.to_csv(result_path, index=False)

    return df

# append the compound vader score to the corresponding news


def read_news_path(df):
    #print('Reading in datasets...')
    cs = []
    # append a compound score to every news row
    for row in range(len(df)):
        cs.append(analyser.polarity_scores(df['news'].iloc[row])['compound'])
    # append the column to original dataset
    df['compound_vader_score'] = cs
    return df


# group by the mean compound vader score by dates
def find_news_pred_label(df, threshold):
    #print('Calling find_pred_label...')
    news = df['news']
    # group the data by dates
    df = df.groupby(['dates'])['compound_vader_score'].mean().reset_index()
    final_label = []

    # convert the vader score using a threshold to a sentiment label
    for i in range(len(df)):

        if df['compound_vader_score'].iloc[i] > threshold:
            final_label.append(2)
        elif df['compound_vader_score'].iloc[i] < -threshold:
            final_label.append(0)
        elif (df['compound_vader_score'].iloc[i] >= -threshold
              and df['compound_vader_score'].iloc[i] <= threshold):
            final_label.append(1)

    df['vader_label'] = final_label
    return df


# merge the dataset with the hang seng index daily moving average
def merge_actual_label(df, hsi_movement_df):
    #print('Calling merge_actual_label...')
    vader_data = df
    vader_data.set_index(keys=["dates"], inplace=True)
    label_data = pd.read_csv(hsi_movement_df)
    label_data.set_index(keys=["dates"], inplace=True)
    # inner join the two datasets using the date index
    merge = pd.merge(vader_data, label_data, how='inner',
                     left_index=True, right_index=True)
    merge = merge.reset_index()
    # drop the redudant column
    merge = merge.drop(['Unnamed: 0'], axis=1)

    return merge
