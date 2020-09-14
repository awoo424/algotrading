from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Bollinger Bands (TSI)
-
Signal line crossover

Buy when price goes below lower band,
sell when price goes above upper band.
"""

class bollinger_bands(Indicator):
    def __init__(self, df, window=20):
        super().__init__(df)
        self.df = df
        self.window = window # signal line window size

    """
    Formula
    -
    Bollinger Bands consist of a middle band with two outer bands:

    Middle Band = 20-day simple moving average (SMA)
    Upper Band = 20-day SMA + (20-day standard deviation of price x 2) 
    Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
    """

    def plot_BB(self):
        # Compute middle band
        self.df['Middle band'] = self.df['Close'].rolling(self.window).mean()

        # Compute 20-day s.d.
        self._mstd = self.df['Close'].rolling(self.window).std(ddof=0)

        # Computer upper and lower bands
        self.df['Upper band'] = self.df['Middle band']  + self._mstd * 2
        self.df['Lower band'] = self.df['Middle band']  - self._mstd * 2

        # Plot graph
        fig = plt.figure()
        self.df['Close'].plot(lw=0.8, label='Closing price')
        self.df['Upper band'].plot(lw=1.2, color='blue', label='Upper band')
        self.df['Lower band'].plot(lw=1.2, color='red', label='Lower band')
        self.df['Middle band'].plot(lw=1.2, color='black', label='Middle band')
        
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['Close'] < self.df['Lower band'], 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['Close'] > self.df['Upper band'], 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
