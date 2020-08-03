import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Moving Average Crossover
-
"""
class MovingAverageCrossover():
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
        signals['signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:] 
                                                    > signals['long_mavg'][self.short_window:], 1.0, 0.0)   
        
        # Generate trading order, buy signal = 1, sell signal = -1
        signals['positions'] = signals['signal'].diff()

        self.signals = signals

        return signals
    
    def plot_signals(self):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Price in $')

        # Plot the closing price
        self.df['Close'].plot(ax=ax1, color='r', lw=2.)

        # Plot the short and long moving averages
        self.signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

        # Plot the buy signals
        ax1.plot(self.signals.loc[self.signals.positions == 1.0].index, 
                self.signals.short_mavg[self.signals.positions == 1.0],
                '^', markersize=10, color='m')
                
        # Plot the sell signals
        ax1.plot(self.signals.loc[self.signals.positions == -1.0].index, 
                self.signals.short_mavg[self.signals.positions == -1.0],
                'v', markersize=10, color='k')

        return fig