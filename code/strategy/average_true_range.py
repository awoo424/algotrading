from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Average True Range (ATR)
-
Signal line crossover

Buy when the TSI crosses above the signal line from below,
sell when the TSI crosses below the signal line from above.

* Signal line: usually a 7 to 12-period EMA of TSI
"""

class atr(Indicator):
    def __init__(self, df, window=14):
        super().__init__(df)
        self.df = df
        self.window = window # signal line window size
        self.array_high = list(self.df['High'])
        self.array_low = list(self.df['Low'])

    """
    Formula
    -
    Current ATR = [(Prior ATR x 13) + Current TR] / n

    1st TR value = High - Low
    1st n-day ATR = average of the daily TR values for the last n days
    """

    def cal_ATR(self, window=14):
        self.window = window

        tr = [None] * len(self.df)

        for i in range(len(self.df)):
            tr[i] = self.array_high[i] - self.array_low[i]

        atr = [None] * len(self.df)
        atr[15] = sum(tr[0:15]) / self.window
        
        for i in range(16,len(self.df)):
            atr[i] = (atr[i-1] * (self.window-1) + tr[i]) / self.window
        
        self.df['ATR'] = atr

    def plot_ATR(self):
        # Plot graph
        fig = plt.figure()
        self.df['ATR'].plot(lw=1.2, color='blue', label='Average True Range (ATR)')
        plt.legend()

        return fig

    """
    Determine if security is highly volatile
    -
    [50-day EMA > 200-day EMA]  AND  [(250-day ATR / 20-day SMA) * 100 < 4] 
    """
    def high_volatility(self):
        exp1 = self.df['Close'].ewm(span=50, adjust=False).mean().tail(1).item()
        exp2 = self.df['Close'].ewm(span=200, adjust=False).mean().tail(1).item()

        exp3 = self.df['Close'].rolling(window=20, min_periods=1, center=False).mean().tail(1).item()
        atr = self.df['ATR'].tail(1).item()

        # debug
        # print(exp1)
        # print(exp2)
        # print(atr / exp3 * 100)

        return (exp1 > exp2) and (atr / exp3 * 100) < 4
