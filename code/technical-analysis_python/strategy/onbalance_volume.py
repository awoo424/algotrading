from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
On-Balance Volume (OBV)
-
"""

class obv(Indicator):
    def __init__(self, df, window=12):
        super().__init__(df)
        self.df = df
        self.window = window # signal line window size

    """
    Formula
    -
    There are 3 cases:

    1) If closing price > prior close price: 
    Current OBV = Previous OBV + Current Volume

    2) If closing price < prior close price: 
    Current OBV = Previous OBV - Current Volume

    3) If closing price = prior close price then:
    Current OBV = Previous OBV (no change)  
    """

    def plot_OBV(self):
        obv = [0] * len(self.df)
        array_close = list(self.df['Close'])
        array_volume = list(self.df['Volume'])

        for i in range(1, len(self.df)):
            if (array_close[i] > array_close[i-1]):
                obv[i] = obv[i-1] + array_volume[i]
            elif (array_close[i] < array_close[i-1]):
                obv[i] = obv[i-1] - array_volume[i]
            else:
                obv[i] = obv[i-1]

        self.df['OBV'] = obv

        # Plot graph
        fig = plt.figure()
        self.df['OBV'].plot(lw=1.2, color='blue', label='On-Balance Volume (OBV)')
        plt.legend()

        return fig
