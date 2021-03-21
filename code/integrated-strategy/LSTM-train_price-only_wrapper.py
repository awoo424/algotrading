"""
Trading signal prediction with LSTM
-
Input: dataframe with daily stock tick
Output: buy (+1) / sell (-1) / neutral (0) signals


Code reference:
https://www.kaggle.com/taronzakaryan/predicting-stock-price-using-lstm-model-pytorch
"""

import numpy as np
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
from utils import read_data, load_data, visualise, gen_signal


def LSTM_predict(symbol):

    data_dir = "../../database/microeconomic_data/hkex_ticks_day/"

    # select date range
    dates = pd.date_range('2010-01-02','2016-12-31',freq='B')
    test_dates = pd.date_range('2017-01-03','2021-03-03',freq='B')

    # select ticker
    symbol = symbol

    # load data
    df = read_data(data_dir, symbol, dates)
    df_test = read_data(data_dir, symbol, test_dates)

    scaler = MinMaxScaler(feature_range=(-1, 1))

    df['Close'] = scaler.fit_transform(df['Close'].values.reshape(-1,1))
    df_test['Close'] = scaler.fit_transform(df_test['Close'].values.reshape(-1,1))

    look_back = 60 # choose sequence length

    x_train, y_train, x_test, y_test = load_data(df, look_back)
    print('x_train.shape = ',x_train.shape)
    print('y_train.shape = ',y_train.shape)
    print('x_test.shape = ',x_test.shape)
    print('y_test.shape = ',y_test.shape)

    # make training and test sets in torch
    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test).type(torch.Tensor)
    y_train = torch.from_numpy(y_train).type(torch.Tensor)
    y_test = torch.from_numpy(y_test).type(torch.Tensor)

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
    input_dim = 1
    hidden_dim = 32
    num_layers = 2 
    output_dim = 1
    torch.manual_seed(1) # set seed

    model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

    loss_fn = torch.nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)

    # check dimensions
    # print(model)
    # print(len(list(model.parameters())))
    # for i in range(len(list(model.parameters()))):
    #     print(list(model.parameters())[i].size())

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
    pred_filename = 'output/' + symbol + '_pred.png'
    visualise(df, y_test, y_test_pred, pred_filename)

    # Inferencing
    y_inf_pred, y_inf = predict_price(df_test, model, scaler)
    signal = gen_signal(y_inf_pred, y_inf)

    # Save signals as csv file
    output_df = pd.DataFrame(index=df_test.index)
    output_df['signal'] = signal
    output_df.index.name = "Date"

    output_filename = 'output/' + symbol + '_output.csv'
    output_df.to_csv(output_filename)

    # Plot inferencing results
    inf_filename = 'output/' + symbol + '_inf.png'
    visualise(df_test, y_inf, y_inf_pred, inf_filename)



def main():
    ticker_list = ['0001', '0002', '0003', '0004', '0005', '0016', '0019', '0113', '0168', '0175', '0386', '0388', '0669', '0700',
                   '0762', '0823', '0857', '0868', '0883', '0939', '0941', '0968', '1211', '1299', '1818', '2319', '2382', '2688', '2689', '2899']
    
    for ticker in ticker_list:

        print("############ Ticker: " + ticker + " ############")
        LSTM_predict(ticker)
        print('\n')

if __name__ == "__main__":
    main()
