import numpy as np
import random
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def read_data(data_dir, symbol, dates):
  df = pd.DataFrame(index=dates)
  
  new_df = pd.read_csv(data_dir+ "hkex_" + symbol  +".csv", index_col='Date', parse_dates=True, usecols=['Date', 'Close'], na_values=['nan'])
  new_df = new_df.rename(columns={'Close': symbol})
  df = df.join(new_df)

  # data pre-processing
  df = df.rename(columns={symbol: 'Close'})
  df = df.fillna(method='ffill')  

  return df

# create train, test data given stock data and sequence length
def load_data(stock, look_back):

    data_raw = stock.values # convert to numpy array
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


def visualise(df, y_test, y_test_pred, output_file):

    figure, axes = plt.subplots(figsize=(15, 6))
    axes.xaxis_date()
    #print(y_test.shape)

    axes.plot(df[len(df)-len(y_test):].index, y_test, color = 'red', label = 'Real HKEX_0001 Stock Price')
    axes.plot(df[len(df)-len(y_test):].index, y_test_pred, color = 'blue', label = 'Predicted HKEX_0001 Stock Price')
    
    plt.title('Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()

    plt.savefig(output_file)
    #plt.show()
  
def gen_signal(pred, actual_output):
    signal = []
    
    for p,a in zip(pred,actual_output):

        if (abs(p - a) < 1.0):
            signal.append(0)
            
        # shows that current price is overvalued, sell the stock
        elif (p > a):
            signal.append(-1)
            
        # shows that current price is undervalued, buy the stock
        elif (p < a):
            signal.append(1)
            
    return signal