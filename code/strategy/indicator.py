import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Indicator:
    def __init__(self, df):
        self.df = df

    def plot_signals(self, signals):
        # Initialize the plot figure
        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111,  ylabel='Price in $')

        # Plot the closing price
        self.df['Close'].plot(ax=ax1, lw=1.2)

        # Plot the buy signals
        ax1.plot(signals.loc[signals.positions == 1.0].index, 
                self.df['Close'][signals.positions == 1.0],
                '^', markersize=8, color='g')
                
        # Plot the sell signals
        ax1.plot(signals.loc[signals.positions == -1.0].index, 
                self.df['Close'][signals.positions == -1.0],
                'v', markersize=8, color='r')

        return fig