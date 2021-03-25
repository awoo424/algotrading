"""
Trading signal prediction with LSTM
-
Input: dataframe with daily stock tick
Output: buy (+1) / sell (-1) / neutral (0) signals


Code reference:
https://www.kaggle.com/taronzakaryan/predicting-stock-price-using-lstm-model-pytorch
"""

import os
import numpy as np
from numpy import zeros, newaxis
import random
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('seaborn')

import datetime
import math, time
import itertools
from math import sqrt
from operator import itemgetter
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

import torch
import torch.nn as nn
from torch.autograd import Variable

from models.LSTM import LSTM, predict_price
from utils import read_strategy_data, load_data, merge_data, visualise, gen_signal


def LSTM_predict(symbol):

    data_dir = "../../database_real/machine_learning_data/"
    sentiment_data_dir = "../../database/sentiment_data/data-result/"


    # Get merged df with stock tick and sentiment scores
    df, scaled, scaler = merge_data(symbol, data_dir, sentiment_data_dir, 'macd-crossover')
    # print(df.index)
    look_back = 60 # choose sequence length

    x_train, y_train, x_test_df, y_test_df = load_data(scaled, look_back)
    print('x_train.shape = ',x_train.shape)
    print('y_train.shape = ',y_train.shape)
    print('x_test.shape = ',x_test_df.shape)
    print('y_test.shape = ',y_test_df.shape)

    # make training and test sets in torch
    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test_df).type(torch.Tensor)
    y_train = torch.from_numpy(y_train).type(torch.Tensor)
    y_test = torch.from_numpy(y_test_df).type(torch.Tensor)

    n_steps = look_back - 1
    batch_size = 32
    num_epochs = 100 # n_iters / (len(train_X) / batch_size)

    
    train = torch.utils.data.TensorDataset(x_train,y_train)
    test = torch.utils.data.TensorDataset(x_test,y_test)

    train_loader = torch.utils.data.DataLoader(dataset=train, 
                                            batch_size=batch_size, 
                                            shuffle=False)

    test_loader = torch.utils.data.DataLoader(dataset=test, 
                                            batch_size=batch_size, 
                                            shuffle=False)

    # Hyperparameters
    input_dim = 7
    hidden_dim = 64 # default = 32
    num_layers = 4 # default = 2 
    output_dim = 7
    torch.manual_seed(1) # set seed

    model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

    loss_fn = torch.nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)

    hist = np.zeros(num_epochs)

    # Number of steps to unroll
    seq_dim = look_back - 1  

    # Train model
    for t in range(num_epochs):    
        # Forward pass
        y_train_pred = model(x_train)
        loss = loss_fn(y_train_pred, y_train)

        if t % 10 == 0 and t !=0:
            print("Epoch ", t, "MSE: ", loss.item())

        hist[t] = loss.item()

        # Zero out gradient, else they will accumulate between epochs
        optimiser.zero_grad()

        # Backward pass
        loss.backward()

        # Update parameters
        optimiser.step()
    
    # plt.plot(hist, label="Training loss")
    # plt.legend()
    # plt.show()
    # plt.savefig('output/0001_training_loss.png')

    # Make predictions
    y_test_pred = model(x_test)

    # Invert predictions
    y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
    y_train = scaler.inverse_transform(y_train.detach().numpy())
    y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
    y_test = scaler.inverse_transform(y_test.detach().numpy())

    # Calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(y_train[:,0], y_train_pred[:,0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(y_test[:,0], y_test_pred[:,0]))
    print('Test Score: %.2f RMSE' % (testScore))

    # Plot predictions
    pred_filename = 'LSTM_output/' + symbol + '_pred.png'
 
    visualise(df, y_test[:,0], y_test_pred[:,0], pred_filename)
    
    signal_dataframe = gen_signal(df[len(df)-len(y_test):].index, y_test_pred[:,0], y_test[:,0])
    #print(signal_dataframe)

    # Save signals as csv file
    output_filename = 'LSTM_output/' + symbol + '_output.csv'
    signal_dataframe.to_csv(output_filename,index=False)


def main():
    # ticker_list = ['0001', '0002', '0003', '0004', '0005', '0016', '0019', '0113', '0168', '0175', '0386', '0388', '0669', '0700',
    #                '0762', '0823', '0857', '0868', '0883', '0939', '0941', '0968', '1211', '1299', '1818', '2319', '2382', '2688', '2689', '2899']
  
    ticker_list = ['0001']

    for ticker in ticker_list:

        print("############ Ticker: " + ticker + " ############")
        LSTM_predict(ticker)
        
        print('\n')

if __name__ == "__main__":
    main() 