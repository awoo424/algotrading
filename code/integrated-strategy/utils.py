import os
import numpy as np
import random
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler


def read_data(data_dir, symbol, dates):
    
  df = pd.DataFrame(index=dates)
  
  new_df = pd.read_csv(data_dir+ "hkex_" + symbol  +".csv", index_col='Date', parse_dates=True, usecols=['Date', 'Close'], na_values=['nan'])
  new_df = new_df.rename(columns={'Close': symbol})
  df = df.join(new_df)

  # data pre-processing
  df = df.rename(columns={symbol: 'Close'})
  df = df.fillna(method='ffill')  
  df = df.fillna(0.0)

  return df

def read_strategy_data(data_dir, symbol, dates, strategy):

  df = pd.DataFrame(index=dates)
  
  new_df = pd.read_csv(data_dir + symbol  + ".HK_" + strategy + ".csv", index_col='Date', parse_dates=True, usecols=['Date', 'Close'], na_values=['nan'])
  new_df = new_df.rename(columns={'Close': symbol})
  df = df.join(new_df)

  # data pre-processing
  df = df.rename(columns={symbol: 'Close'})
  df = df.fillna(method='ffill')  
  df = df.fillna(0.0)

  return df

# create train, test data given stock data and sequence length
def load_data(data_raw, look_back):
    data = []
    
    # create all possible sequences of length seq_len
    for index in range(len(data_raw) - look_back): 
        data.append(data_raw[index: index + look_back])
    
    data = np.array(data)
    test_set_size = int(np.round(0.2*data.shape[0]))
    train_set_size = data.shape[0] - (test_set_size)
    
    x_train = data[:train_set_size,:-1,:]
    y_train = data[:train_set_size,-1,:]
    
    x_test = data[train_set_size:,:-1]
    y_test = data[train_set_size:,-1,:]
    
    return [x_train, y_train, x_test, y_test]
 

# return dataframe with stock tick and sentiment scores 
def merge_data(ticker, data_dir, sentiment_data_dir, strategy, start_date=None, end_date=None):
    merge_path = os.path.join(data_dir,ticker.zfill(4)+'.HK_' + strategy + '.csv') 
 
    sentiment_path = os.path.join(sentiment_data_dir,'data-'+ticker.zfill(5)+'-result.csv') 
    sentiment_df = pd.read_csv(sentiment_path,index_col='dates',parse_dates=['dates'], na_values=['nan'])
    merge_df = pd.read_csv(merge_path,index_col='Date',usecols=['Date','signal','GDP','Unemployment rate','Property price','Close'],parse_dates=['Date'], na_values=['nan'])

    merge_df = merge_df.rename(columns={'signal': 'technical_signal'})
    
    df = pd.merge(merge_df,sentiment_df, how='inner', left_index=True, right_index=True)

    if (start_date != None) and (end_date != None):
        df = df.loc[pd.Timestamp(start_date):pd.Timestamp(end_date)]

    # pre-processing
    df = df.fillna(method='ffill')
    values = df.values

    # ensure all data is float
    values = values.astype('float32')
    # normalise features
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled = scaler.fit_transform(values)

    return df, scaled, scaler

def visualise(df, y_test, y_test_pred, output_file):
    pd.plotting.register_matplotlib_converters()
    figure, axes = plt.subplots(figsize=(15, 6))
    axes.xaxis_date()
    #print(y_test.shape)

    axes.plot(df[len(df)-len(y_test):].index, y_test, color = 'red', label = 'Real Stock Price')
    axes.plot(df[len(df)-len(y_test):].index, y_test_pred, color = 'blue', label = 'Predicted Stock Price')
    
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()

    plt.savefig(output_file)
    # plt.show()
  
def gen_signal(pred, actual_output, dates, by_trend=False):
    output_df = pd.DataFrame()
    signal = []

    # print(pred)
    # print(actual_output)

    if (by_trend): # generate signals by trend

        pred_trend = [ (j - i) / j for i, j in zip(pred[:-1], pred[1:]) ]
        pred_trend.append(0.0) # for last element

        actual_trend = [ (j - i) / j for i, j in zip(actual_output[:-1], actual_output[1:]) ]
        actual_trend.append(0.0) # for last element

        for p,a in zip(pred_trend, actual_trend):

            if np.sign(p) == np.sign(a):
                signal.append(0)
                
            # shows that current price is overvalued, sell the stock
            elif (np.sign(p) == -1) and (np.sign(a) == 1):
                signal.append(-1)
                
            # shows that current price is undervalued, buy the stock
            elif (np.sign(p) == 1) and (np.sign(a) == -1):
                signal.append(1)

            else: # in case of zeroes
                signal.append(0)

    else: # generate signals by abs price

        for p,a in zip(pred, actual_output):

            if (abs(p - a) < 1.0):
                signal.append(0)
                
            # shows that current price is overvalued, sell the stock
            elif (p > a):
                signal.append(-1)
                
            # shows that current price is undervalued, buy the stock
            elif (p < a):
                signal.append(1)
         
    #print(len(signal))
    output_df['Date'] = dates

    output_df['signal']=  signal  
    
    return output_df