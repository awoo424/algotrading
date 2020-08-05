from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Relative Strength Index (RSI)
-
Buy when RSI crosses the lower threshold (30),
sell when RSI crosses the upper threshold (70).
"""
class rsi(Indicator):
    def __init__(self, df, window_length=14):
        super().__init__(df)
        self.df = df
        self.mean = 'ewma'
        self.window_length = window_length
        self.lower = 30
        self.upper = 70

    """
    Formula
    -
    RSI = 100 - 100 / (1 + RS)

    RS = Average Gain / Average Loss
    """
    def plot_RSI(self):
        # Get just the adjusted close
        close = self.df['Close']
        # Get the difference in price from previous step
        delta = close.diff()
        # Get rid of the first row
        delta = delta[1:] 

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        if self.mean == 'ewma':
            # Calculate the EWMA
            roll_up = up.ewm(span=self.window_length).mean()
            roll_down = down.abs().ewm(span=self.window_length).mean()

            # Calculate the RSI based on EWMA
            RS = roll_up / roll_down
            self.RSI = 100.0 - (100.0 / (1.0 + RS))

        else:
            # Calculate the SMA
            roll_up = up.rolling(self.window_length).mean()
            roll_down = down.abs().rolling(self.window_length).mean()

            # Calculate the RSI based on SMA
            RS = roll_up / roll_down
            self.RSI = 100.0 - (100.0 / (1.0 + RS))
        
        # Plot graph
        fig = plt.figure()
        self.RSI.plot(lw=1.2)

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0
        signals['RSI'] = self.RSI

        # Generate buy signal
        signals.loc[signals['RSI'] < self.lower, 'signal'] = 1.0
        
        # Generate sell signal
        signals.loc[signals['RSI'] > self.upper, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals