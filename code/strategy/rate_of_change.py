from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Rate of Change (ROC)
-
Buy when RSI crosses the lower threshold (-30), (oversold)
sell when ROC crosses the upper threshold (+30). (overbought)
"""
class roc(Indicator):
    def __init__(self, df, n=12):
        super().__init__(df)
        self.df = df
        self.n = 12 # short-term smaller e.g. 9, long-term larger e.g. 200
        self.lower = -8 # thesholds vary by asset traded
        self.upper = 8

    """
    Formula
    -
    ROC = [(Closing price - Closing price n periods ago) / (Closing price n periods ago)] * 100
    """
    def plot_ROC(self):
        # Calculate difference between closing price and 
        # closing price n period ago
        diff = self.df['Close'].diff(self.n - 1)

        # Calculate closing price n periods ago
        closing = self.df['Close'].shift(self.n - 1)

        self.df['ROC'] = (diff / closing) * 100

        # Plot graph
        fig = plt.figure()
        self.df['ROC'].plot(lw=1.2, label='Rate of Change (ROC)')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0
        signals['ROC'] = self.df['ROC']

        # Generate buy signal
        signals.loc[signals['ROC'] < self.lower, 'signal'] = 1.0
        
        # Generate sell signal
        signals.loc[signals['ROC'] > self.upper, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals