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

from utils.data_utils import read_data, load_data


# load data
data_dir = "../../database/microeconomic_data/hkex_ticks_day/"

dates = pd.date_range('2010-01-02','2016-12-31',freq='B')
test_dates = pd.date_range('2017-01-03','2020-09-30',freq='B')
symbols = ["0001"]

df_0001 = read_data(data_dir, symbols, dates)
df_0001_test = read_data(data_dir, symbols, test_dates)

df_0001 = df_0001.rename(columns={'0001': 'Close'})
df_0001_test = df_0001_test.rename(columns={'0001': 'Close'})
df_0001 = df_0001.fillna(method='ffill')
df_0001_test= df_0001_test.fillna(method='ffill')

scaler = MinMaxScaler(feature_range=(-1, 1))
df_0001['Close'] = scaler.fit_transform(df_0001['Close'].values.reshape(-1,1))
df_0001_test['Close'] = scaler.fit_transform(df_0001_test['Close'].values.reshape(-1,1))

# print(df_0001_test.head())
# print(df_0001.head())

look_back = 60 # choose sequence length

x_train, y_train, x_test, y_test = load_data(df_0001, look_back)
print('x_train.shape = ',x_train.shape)
print('y_train.shape = ',y_train.shape)
print('x_test.shape = ',x_test.shape)
print('y_test.shape = ',y_test.shape)

# make training and test sets in torch
x_train = torch.from_numpy(x_train).type(torch.Tensor)
x_test = torch.from_numpy(x_test).type(torch.Tensor)
y_train = torch.from_numpy(y_train).type(torch.Tensor)
y_test = torch.from_numpy(y_test).type(torch.Tensor)

n_steps = look_back-1
batch_size = 32
num_epochs = 100 #n_iters / (len(train_X) / batch_size)

train = torch.utils.data.TensorDataset(x_train,y_train)
test = torch.utils.data.TensorDataset(x_test,y_test)

train_loader = torch.utils.data.DataLoader(dataset=train, 
                                           batch_size=batch_size, 
                                           shuffle=False)

test_loader = torch.utils.data.DataLoader(dataset=test, 
                                          batch_size=batch_size, 
                                          shuffle=False)

# model

# Hyperparameters
input_dim = 1
hidden_dim = 32
num_layers = 2 
output_dim = 1


# Here we define our model as a class
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTM, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.num_layers = num_layers

        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 32, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states! 
        out = self.fc(out[:, -1, :]) 
        # out.size() --> 100, 10
        return out
    
model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

loss_fn = torch.nn.MSELoss()

optimiser = torch.optim.Adam(model.parameters(), lr=0.01)

# check dimensions
# print(model)

# print(len(list(model.parameters())))
# for i in range(len(list(model.parameters()))):
#     print(list(model.parameters())[i].size())

# train model

hist = np.zeros(num_epochs)

# Number of steps to unroll
seq_dim = look_back - 1  

for t in range(num_epochs):
    # Initialise hidden state
    # Don't do this if you want your LSTM to be stateful
    #model.hidden = model.init_hidden()
    
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
# plt.savefig('ML-model-output/HKEX_0001_training_loss.png')


# make predictions
y_test_pred = model(x_test)

# invert predictions
y_train_pred = scaler.inverse_transform(y_train_pred.detach().numpy())
y_train = scaler.inverse_transform(y_train.detach().numpy())
y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
y_test = scaler.inverse_transform(y_test.detach().numpy())


# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(y_train[:,0], y_train_pred[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(y_test[:,0], y_test_pred[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# Visualising the results
def visualization(df,y_test,y_test_pred):
    figure, axes = plt.subplots(figsize=(15, 6))
    axes.xaxis_date()
    print(y_test.shape)

    axes.plot(df[len(df)-len(y_test):].index, y_test, color = 'red', label = 'Real HKEX_0001 Stock Price')
    axes.plot(df[len(df)-len(y_test):].index, y_test_pred, color = 'blue', label = 'Predicted HKEX_0001 Stock Price')
    #axes.xticks(np.arange(0,394,50))
    plt.title('HKEX_0001 Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('HKEX_0001 Stock Price')
    plt.legend()
    plt.savefig('ML-model-output/HKEX_0001_pred.png')
    #plt.show()

visualization(df_0001,y_test,y_test_pred)
