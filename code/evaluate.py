import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Portfolio return
"""
def PortfolioReturn(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']

    # Create a figure
    fig = plt.figure()

    # Plot the results
    returns.plot(lw=1.2, label='Portfolio return')
    plt.legend()

    return fig

"""
Sharpe ratio
"""
def SharpeRatio(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']

    if (returns.std() != 0):
        # annualised Sharpe ratio
        sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    else:
        sharpe_ratio = 0
        
    return sharpe_ratio

"""
Maximum drawdown

:window: trailing 252 trading day window
"""
def MaxDrawdown(df, window=252):
    # Calculate the max drawdown in the past window days for each day 
    rolling_max = df['Close'].rolling(window, min_periods=1).max()
    daily_drawdown = df['Close'] / rolling_max - 1.0

    # Calculate the minimum (negative) daily drawdown
    max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

    # Create a figure
    fig = plt.figure()

    # Plot the results
    daily_drawdown.plot(lw=1.2, label='Daily drawdown')
    max_daily_drawdown.plot(lw=1.2, label='Max daily drawdown')
    plt.legend()

    return fig, max_daily_drawdown, daily_drawdown

"""
Compound Annual Growth Rate (CAGR)

Formula
-
(Ending value / Beginning value) ** (1/n) - 1
"""

def CAGR(portfolio):
    # Get the number of days in df
    days = (portfolio.index[-1] - portfolio.index[0]).days

    # Calculate the CAGR 
    cagr = (((portfolio['total'][-1] / portfolio['total'][0])) ** (252.0 / days)) - 1

    return cagr

"""
Standard Deviation (SD)

Formula
- 
sqrt(sum[(r_i - r_avg)^2] / n-1)
"""

def StandardDeviation(portfolio):
    # Isolate the returns of your strategy
    returns = portfolio['returns']
    
    returns_diff = returns - returns.mean()
    returns_diff = returns_diff * returns_diff
    returns_diff_sum = returns_diff.sum()
    
    # annualized sd
    sd = math.sqrt(returns_diff_sum / (len(returns) - 1))

    return sd
