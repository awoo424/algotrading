from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Standard deviation (SD)
"""

class sd(Indicator):
    def __init__(self, df, window=21):
        super().__init__(df)
        self.df = df
        self.window = window # signal line window size
        self.trading_days = 252  # trading days per year

    """
    Formula
    -
    Current ATR = [(Prior ATR x 13) + Current TR] / n

    1st TR value = High - Low
    1st n-day ATR = average of the daily TR values for the last n days
    """

    def cal_SD(self, window=21, r_demeaned=True):
        self.window = window

        self.df['SD'] = self.df['Close'].rolling(self.window).std(ddof=0)

        return self.df['SD'].tail(1).item()

    def plot_SD(self):
        # Plot graph
        fig = plt.figure()
        self.df['SD'].plot(lw=1.2, color='blue', label='Standard Deviation (SD)')
        self.df['Close'].plot(lw=0.8, color='black', label='Closing price')
        plt.legend()

        return fig
