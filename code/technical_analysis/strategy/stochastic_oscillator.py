from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Stochastic Oscillator (STC)
-
Buy when %K line crosses above the %D line,
sell when %K line crosses below the %D line.
"""

class stc_oscillator(Indicator):
    def __init__(self, df, k=14, d=3):
        super().__init__(df)
        self.df = df
        self.k = k  # k periods default = 14
        self.d = d

    """
    Formula
    -
    %K = (Current Close - Lowest Low) / (Highest High - Lowest Low) * 100
    %D = 3-day SMA of %K

    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period
    %K is multiplied by 100 to move the decimal point two places
    """

    def plot_KD(self):
        length = len(self.df)
        array_dates = list(self.df.index)
        array_high = list(self.df['High'])
        array_low = list(self.df['Low'])
        array_close = list(self.df['Close'])
        array_open = list(self.df['Open'])
        array_volume = list(self.df['Volume'])

        array_highest = [0] * length # store highest highs

        for i in range(self.k - 1, length):
            highest = array_high[i]

            for j in range(i - 13, i + 1): # k-day lookback period
                if array_high[j] > highest:
                    highest = array_high[j]
            
            array_highest[i] = highest
        
        array_lowest = [0] * length # store lowest lows

        for i in range(self.k - 1, length):
            lowest = array_low[i]

            for j in range(i - 13, i + 1): # k-day lookback period
                if array_low[j] > lowest:
                    lowest = array_low[j]
            
            array_lowest[i] = lowest

        # find %K line values
        kvalues = [0] * length

        for i in range(self.k - 1, length):
            k = ((array_close[i] - array_lowest[i]) * 100 ) / (array_highest[i] - array_lowest[i])
            # Kvalue.append(k)
            kvalues[i] = k

        self.df['%K'] = kvalues

        # %D = 3-day SMA of %K
        self.df['%D'] = self.df['%K'].rolling(window=3, min_periods=1, center=False).mean()

        # Plot graph
        fig = plt.figure()
        self.df['%K'].plot(lw=1.2, color='red', label='%K line')
        self.df['%D'].plot(lw=1.2, color='blue', label='%D line')

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0
        signals['%K'] = self.df['%K']
        signals['%D'] = self.df['%D']

        # Generate buy signal
        signals.loc[signals['%K'] > signals['%D'], 'signal'] = 1.0

        # Generate sell signal
        signals.loc[signals['%K'] < signals['%D'], 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
