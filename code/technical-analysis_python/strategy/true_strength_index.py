from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
True Strength Index (TSI)
-
Signal line crossover

Buy when the TSI crosses above the signal line from below,
sell when the TSI crosses below the signal line from above.

* Signal line: usually a 7 to 12-period EMA of TSI
"""

class tsi(Indicator):
    def __init__(self, df, window=12):
        super().__init__(df)
        self.df = df
        self.window = window # signal line window size

    """
    Formula
    -
    TSI = (Double Smoothed PC / Double Smoothed Absolute PC) x 100

    Double Smoothed PC
    ------------------
    PC = Current Price minus Prior Price
    First Smoothing = 25-period EMA of PC
    Second Smoothing = 13-period EMA of 25-period EMA of PC

    Double Smoothed Absolute PC
    ---------------------------
    Absolute Price Change |PC| = Absolute Value of Current Price minus Prior Price
    First Smoothing = 25-period EMA of |PC|
    Second Smoothing = 13-period EMA of 25-period EMA of |PC|
    """

    def plot_TSI(self):
        # Compute TSI
        pc = self.df['Close'] - self.df['Close'].shift(1) # price change

        self.df['Double Smoothed PC'] = pc.ewm(span=25, adjust=False).mean().ewm(
            span=13, adjust=False).mean()

        self.df['Double Smoothed Abs PC'] = abs(pc).ewm(span=25, adjust=False).mean().ewm(
            span=13, adjust=False).mean()

        self.df['TSI'] =  self.df['Double Smoothed PC'] / self.df['Double Smoothed Abs PC'] * 100

        # Signal line
        self.df['Signal line'] = self.df['TSI'].ewm(span=self.window, adjust=False).mean()

        # Plot graph
        fig = plt.figure()
        self.df['TSI'].plot(lw=1.2, color='blue', label='True Strength Index (TSI)')
        self.df['Signal line'].plot(lw=1.2, color='red', label='Signal line')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['TSI'] > self.df['Signal line'], 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['TSI'] < self.df['Signal line'], 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
