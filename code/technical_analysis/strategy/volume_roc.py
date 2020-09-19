from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Volume Rate of Change
-
Buy if volume rate of change goes below zero;
sell if volume rate of change goes above zero.
"""

class volume_roc(Indicator):
    def __init__(self, df, n=25):
        super().__init__(df)
        self.df = df
        self.n = n # lookback period

    """
    Formula
    -
    ( Volume [today] - Volume [n days ago] ) / Volume [n days ago]
    """

    def plot_VROC(self):
        self.df['Volume ROC'] = ((self.df['Close'] - self.df['Close'].shift(self.n)) / self.df['Close'].shift(self.n))

        # Plot graph
        fig = plt.figure()
        self.df['Volume ROC'].plot(lw=1.2, color='blue', label='Volume Rate of Change')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['Volume ROC'] < 0, 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['Volume ROC'] > 0, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
