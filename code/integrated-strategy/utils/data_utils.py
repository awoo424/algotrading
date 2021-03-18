import numpy as np
import random
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def read_data(data_dir, symbols, dates):
  df = pd.DataFrame(index=dates)
  for symbol in symbols:
    new_df = pd.read_csv(data_dir+ "hkex_" + symbol  +".csv", index_col='Date', parse_dates=True, usecols=['Date', 'Close'], na_values=['nan'])
    new_df = new_df.rename(columns={'Close': symbol})
    df = df.join(new_df)
  return df

# function to create train, test data given stock data and sequence length
def load_data(stock, look_back):

    data_raw = stock.values # convert to numpy array
    print(data_raw.shape)
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