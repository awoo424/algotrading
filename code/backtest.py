import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def Backtest(ticker, signals, df, initial_capital=float(100000.0)):
    # Create a DataFrame `positions`
    positions = pd.DataFrame(index=signals.index).fillna(0.0)

    # Buy a 100 shares
    positions[ticker] = 100*signals['signal']   
    
    # Initialize the portfolio with value owned   
    portfolio = positions.multiply(df['Close'], axis=0)

    # Store the difference in shares owned 
    pos_diff = positions.diff()

    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(df['Close'], axis=0)).sum(axis=1)

    # Add `cash` to portfolio
    portfolio['cash'] = initial_capital - (pos_diff.multiply(df['Close'], axis=0)).sum(axis=1).cumsum()   

    # Add `total` to portfolio
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']

    # Add `returns` to portfolio
    portfolio['returns'] = portfolio['total'].pct_change()

    # Plot portfolio value

    # Create a figure
    fig = plt.figure(figsize=(8, 6))
    fig.set_size_inches(8, 6)

    ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

    # Plot the equity curve in dollars
    portfolio['total'].plot(ax=ax1, lw=1.2, label='Total value (including cash)')
    

    positions = signals.positions.to_numpy()

    ax1.plot(portfolio.loc[positions == 1.0].index, 
            portfolio.total[positions == 1.0],
            '^', markersize=8, color='g', label='Buy signal')
    ax1.plot(portfolio.loc[positions == -1.0].index, 
            portfolio.total[positions == -1.0],
            'v', markersize=8, color='r', label='Sell signal')

    plt.legend()
    
    return portfolio, fig
