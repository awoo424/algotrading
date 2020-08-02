import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Sharpe ratio
"""
def SharpeRatio(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']

    # annualized Sharpe ratio
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

    return sharpe_ratio

"""
Maximum dropdown

:window: trailing 252 trading day window
"""
def MaxDropdown(df, window=252):
    # Calculate the max drawdown in the past window days for each day 
    rolling_max = df['Close'].rolling(window, min_periods=1).max()
    daily_drawdown = df['Close']/rolling_max - 1.0

    # Calculate the minimum (negative) daily drawdown
    max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

    # Create a figure
    fig = plt.figure()

    # Plot the results
    daily_drawdown.plot()
    max_daily_drawdown.plot()

    return fig

"""
Compound Annual Growth Rate (CAGR)
"""

def CAGR(df):
    # Get the number of days in df
    days = (df.index[-1] - df.index[0]).days

    # Calculate the CAGR 
    cagr = ((((df['Close'][-1]) / df['Close'][1])) ** (365.0/days)) - 1

    return cagr