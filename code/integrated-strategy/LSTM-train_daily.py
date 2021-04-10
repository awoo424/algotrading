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
from utils import read_strategy_data, load_data, merge_data_daily, visualise, gen_signal


def LSTM_predict(symbol, strategy, dir_name):

    data_dir = os.path.join(dir_name,"database_real/machine_learning_data/")
    sentiment_data_dir=os.path.join(dir_name,"database/sentiment_data/data-result/")

    # data_dir = os.path.join(dir_name,"database_real/machine_learning_data/")
    # data_dir = os.path.join(dir_name,'data-results/')

    # Get merged df with stock tick and sentiment scores
    df, scaled, scaler = merge_data_daily(symbol, data_dir, sentiment_data_dir, strategy)
    # print(df.index)

    look_back = 60 # choose sequence length

    x_train, y_train, x_test_df, y_test_df = load_data(scaled, look_back)

    # make training and test sets in torch
    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test_df).type(torch.Tensor)
    y_train = torch.from_numpy(y_train).type(torch.Tensor)
    y_test = torch.from_numpy(y_test_df).type(torch.Tensor)

    # Hyperparameters
    input_dim = 6
    hidden_dim = 64 # default = 32
    num_layers = 4 # default = 2 
    output_dim = 6
    torch.manual_seed(1) # set seed
    num_epochs = 100  # n_iters / (len(train_X) / batch_size)
    lr = 0.01
    batch_size = 72

    print("Hyperparameters:")
    print("input_dim: ", input_dim, ", hidden_dim: ", hidden_dim, ", num_layers: ", num_layers, ", output_dim", output_dim)
    print("num_epochs: ", num_epochs, ", batch_size: ", batch_size, ", lr: ", lr)

    train = torch.utils.data.TensorDataset(x_train,y_train)
    test = torch.utils.data.TensorDataset(x_test,y_test)

    train_loader = torch.utils.data.DataLoader(dataset=train,
                                           batch_size=batch_size,
                                           shuffle=False)

    test_loader = torch.utils.data.DataLoader(dataset=test,
                                          batch_size=batch_size,
                                          shuffle=False)

    model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

    loss_fn = torch.nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)

    hist = np.zeros(num_epochs)

    # Number of steps to unroll
    seq_dim = look_back - 1  

    # Train model
    for t in range(num_epochs):
        for i, (train_data, train_label) in enumerate(train_loader):
            # Forward pass
            train_pred = model(train_data)
            loss = loss_fn(train_pred, train_label)

            hist[t] = loss.item()

            # Zero out gradient, else they will accumulate between epochs
            optimiser.zero_grad()

            # Backward pass
            loss.backward()

            # Update parameters
            optimiser.step()

        if t % 10 == 0 and t != 0:
            y_train_pred = model(x_train)
            loss = loss_fn(y_train_pred, y_train)
            print("Epoch ", t, "MSE: ", loss.item())
    
    # Plot training loss
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

    # visualise(df, y_test[:,0], y_test_pred[:,0])

    return y_train_pred, y_train, y_test_pred, y_test,model


def main():         
    dir_name = os.getcwd() # get current working directory
    ticker = '0001'

    y_train_pred, y_train, y_test_pred, y_test,model = LSTM_predict(ticker, 'macd-crossover', dir_name)
    
    # save model
    torch.save(model, 'saved_models/' + ticker + '_model') 
    model_path = os.path.join(dir_name,'/models' + ticker + '_model')


if __name__ == "__main__":
    main() 