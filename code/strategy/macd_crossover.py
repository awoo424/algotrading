import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Moving Average Convergence Divergence (MACD) crossovers
-
Buy when MACD crosses above the signal line, (bullish crossover)
sell when MACD crosses below the signal line. (bearish crossover)
"""
class macdCrossover():
    def __init__(self, df):
        self.df = df

    def plot_MACD(self):
        exp1 = self.df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['Close'].ewm(span=26, adjust=False).mean()
        self.df['MACD'] = exp1 - exp2
        self.df['Signal line'] = self.df['MACD'].ewm(span=9, adjust=False).mean()

        fig = plt.figure()
        plt.plot(self.df.index, self.df['MACD'], label='MACD', color = '#CA0020')
        plt.plot(self.df.index, self.df['Signal line'], label='Signal Line', color='#0571b0')
        plt.legend(loc='upper left')

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate signals
        signals['signal'] = np.where(self.df['MACD'] > self.df['Signal line'], 1.0, 0.0)   
        
        # Generate trading order, buy signal = 1, sell signal = -1
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals
    
    def plot_signals_MACD(self):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Price in $')

        # Plot MACD and signal line
        self.df[['MACD', 'Signal line']].plot(ax=ax1, lw=2.)

        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index, 
                self.df['MACD'][self.signals.positions == 1.0],
                '^', markersize=10, color='m')
                
        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index, 
                self.df['MACD'][self.signals.positions == -1.0],
                'v', markersize=10, color='k')

        return fig
    
    def plot_signals(self):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Price in $')

        # Plot the closing price
        self.df['Close'].plot(ax=ax1, color='r', lw=1.2)

        # Plot MACD and signal line
        # self.df[['MACD', 'Signal line']].plot(ax=ax1, lw=2.)

        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index, 
                self.df['Close'][self.signals.positions == 1.0],
                '^', markersize=10, color='m')
                
        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index, 
                self.df['Close'][self.signals.positions == -1.0],
                'v', markersize=10, color='k')

        return fig