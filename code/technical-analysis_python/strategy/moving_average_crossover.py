from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Moving Average Crossover
-
Buy when short-term moving average > long-term moving average,
sell when short-term moving average < long-term moving average.
"""
class MovingAverageCrossover(Indicator):
    def __init__(self, df, short_window=40, long_window=100):
        self.df = df
        self.short_window = short_window
        self.long_window = long_window

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Create short simple moving average over the short window
        signals['short_mavg'] = self.df['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()

        # Create long simple moving average over the long window
        signals['long_mavg'] = self.df['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Generate signals
        if (len(signals['short_mavg']) > self.short_window and len(signals['long_mavg']) > self.short_window):
            signals['signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:] 
                                                    > signals['long_mavg'][self.short_window:], 1.0, 0.0)   
        
        # Generate trading order, buy signal = 1, sell signal = -1
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals