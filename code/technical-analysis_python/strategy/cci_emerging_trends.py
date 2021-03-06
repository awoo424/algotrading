from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Commodity Channel Index (CCI) emerging trends
-
Buy when CCI surges above +100, sell when it plunges below -100
"""
class cciEmergingTrends(Indicator):
    def __init__(self, df, window_size=14):
        self.df = df
        self.window_size = window_size
        self.constant = 0.015

    """
    Formula
    -
    CCI = (Typical Price - x-period SMA of TP) / (Constant x Mean Deviation)

    Typical Price (TP) = (High + Low + Close) / 3
    Constant = 0.015
    
    x: Window size (default = 14)
    SMA: Simple Moving Average
    """

    def plot_CCI(self):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Value')

        # Plot CCI
        self.signals['CCI'].plot(ax=ax1, lw=1.2)

        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index,
                 self.signals['CCI'][self.signals.positions == 1.0],
                 '^', markersize=8, color='g')

        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index,
                 self.signals['CCI'][self.signals.positions == -1.0],
                 'v', markersize=8, color='r')

        return fig

    def gen_signals(self):
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        signals['Typical price'] = (
            self.df['High'] + self.df['Low'] + self.df['Close']) / 3

        signals['SMA'] = signals['Typical price'].rolling(
            window=self.window_size, min_periods=1, center=False).mean()

        signals['mean_deviation'] = signals['Typical price'].rolling(
            window=20, min_periods=1, center=False).std()

        signals['CCI'] = (signals['Typical price'] - signals['SMA']) / \
        (self.constant * signals['mean_deviation'])

        # Generate buy signal
        signals.loc[signals['CCI'] > 100, 'signal'] = 1.0

        # Generate sell signal
        signals.loc[signals['CCI'] < -100, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals
