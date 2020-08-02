import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Commodity Channel Index (CCI) correction
-
TL;DR Buy when CCI surges above +100, sell when it plunges below -100
"""
class cciCorrection():
    def __init__(self, df, window_size=20, up=0.015, down=0.015):
        self.df = df
        self.window_size = window_size
        self.up = up
        self.down = down
        self.constant = 0.015

    def step(self, price):
        self.memory.append(price)
        if len(self.memory) < self.window_size:
            return 0

        CCI = (price - np.mean(self.memory))/(0.015*np.std(self.memory))

        # Buy
        if(CCI > 100):
            return 1

        # Sell
        if(CCI < (-100)):
            return -1

        # Hold
        return 0

    """
    Formula
    -
    CCI = (Typical Price - x-period SMA of TP) / (Constant x Mean Deviation)

    x = Window size (default = 20)
    SMA = Simple Moving Average
    Typical Price (TP) = (High + Low + Close) / 3
    Constant = 0.015
    """

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

    def plot_signals(self):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Price in $')

        # Plot the closing price
        self.df['Close'].plot(ax=ax1, color='r', lw=2.)

        # Plot the short and long moving averages
        self.signals['CCI'].plot(ax=ax1, lw=2.)

        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index,
                 self.signals.CCI[self.signals.positions == 1.0],
                 '^', markersize=10, color='m')

        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index,
                 self.signals.CCI[self.signals.positions == -1.0],
                 'v', markersize=10, color='k')

        return fig
