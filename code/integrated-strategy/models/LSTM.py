import numpy as np
from numpy import zeros, newaxis
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from torch.autograd import Variable

class LSTM(nn.Module):

    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):

        super(LSTM, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, dropout=0.4, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialise hidden state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()

        # Initialise cell state
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

def predict_price(data, model, scaler):
    #print(data)

    actual_output = data.values
    #print(actual_output)
    
    #actual_output = torch.from_numpy(actual_output).type(torch.Tensor)
    train_input = actual_output[:,:,newaxis]
    train_input = np.array(train_input)
    train_input = torch.from_numpy(train_input).type(torch.Tensor)

    # make prediction of the input 
    pred = model(train_input)

    # invert predictions
    pred = scaler.inverse_transform(pred.detach().numpy())
    actual_output = scaler.inverse_transform(actual_output.detach().numpy())
    #print(pred.shape)
    
    return pred, actual_output

def predict_price_daily(data, model, scaler):
    #print(data)
    # scaler = MinMaxScaler(feature_range=(-1, 1))
    # train_input = scaler
    
    # print('actual_output',actual_output)
    
    #actual_output = torch.from_numpy(actual_output).type(torch.Tensor)
    train_input = data[:,newaxis,:]
  
    # print('train_inputd',train_input.shape)
    train_input = np.array(train_input)
    train_input = torch.from_numpy(train_input).type(torch.Tensor)
    # train_input  = scaler.inverse_transform(y_test_pred.detach().numpy())
    # make prediction of the input 
    pred = model(train_input)
    # print(pred)
    # invert predictions
    pred = scaler.inverse_transform(pred.detach().numpy())
    # actual_output = scaler.inverse_transform(actual_output.detach().numpy())
    #print(pred.shape)
    
    return pred