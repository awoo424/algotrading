from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Commodity Channel Index (CCI) overbought & oversold
-
Buy when 14-day CCI falls below -100 and then rises back above, 
sell when it rises above +100 and then falls back below.
"""
class cciOverboughtOversold(Indicator):
    def __init__(self, df, window_size=14):
        self.df = df
        self.window_size = window_size
        self.constant = 0.015

    """
    Formula
    -
    CCI = (Typical Price - x-period SMA of TP) / (Constant x Mean Deviation)

    x = Window size (default = 20)
    SMA = Simple Moving Average
    Typical Price (TP) = (High + Low + Close) / 3
    Constant = 0.015
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
                    '^', markersize=10, color='m')

        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index,
                    self.signals['CCI'][self.signals.positions == -1.0],
                    'v', markersize=10, color='k')

        return fig

    def gen_signals(self):
        signals = pd.DataFrame(index=self.df.index)
        signals['label'] = 0.0
        signals['signal'] = 0.0

        signals['Typical price'] = (
            self.df['High'] + self.df['Low'] + self.df['Close']) / 3

        signals['SMA'] = signals['Typical price'].rolling(
            window=self.window_size, min_periods=1, center=False).mean()

        signals['mean_deviation'] = signals['Typical price'].rolling(
            window=20, min_periods=1, center=False).std()

        signals['CCI'] = (signals['Typical price'] - signals['SMA']) / \
        (self.constant * signals['mean_deviation'])

        # Mark when CCI falls below -100
        signals.loc[signals['CCI'] < -100, 'label'] = -1.0

        # Mark when CCI surges above +100
        signals.loc[signals['CCI'] > 100, 'label'] = 1.0

        signals['signal'] = signals['label'].diff()

        # filter trading pos as only if there is change in signal
        signals['tmp_positions'] = 0.0

        for i in range(len(signals)):
            # CCI rises back above -100, buy signal
            if (signals['signal'][i] == 1.0) and (signals['label'][i-1] == -1.0):
                signals['tmp_positions'][i] = 1.0
            # CCI falls back below +100, sell signal
            elif (signals['signal'][i] == -1.0) and (signals['label'][i-1] == 1.0):
                signals['tmp_positions'][i] = -1.0
        
        # Get index of first buy signal
        buy_timestamp = signals[signals['tmp_positions'] == 1.0].index[0]
        buy_index = signals.index.get_loc(buy_timestamp)

        signals['positions'] = 0.0
        signals['positions'][buy_index] = 1.0
        prev_signal = 1.0

        for i in range(buy_index+1, len(signals)):
            if signals['tmp_positions'][i] != 0.0:
                if signals['tmp_positions'][i] != prev_signal:
                    signals['positions'][i] = signals['tmp_positions'][i]
                    prev_signal = signals['tmp_positions'][i]

        self.signals = signals

        return signals
