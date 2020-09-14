from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Williams %R (or just %R)
-
Signal line crossover

Buy when %R goes below -80, (oversold)
sell when %R goes above -20. (overbought)
"""

class williamsR(Indicator):
    def __init__(self, df, lbp=14):
        super().__init__(df)
        self.df = df
        self.lbp = lbp # lookback period

    """
    Formula
    -
    %R = (Highest High - Close) / (Highest High - Lowest Low) * -100

    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period

    Note: %R is multiplied by -100 to correct the inversion and move the decimal
    """

    def plot_wr(self):
        # Compute %R
        hh = self.df['High'].rolling(self.lbp).max()  # highest high over lookback period
        ll = self.df['Low'].rolling(self.lbp).min()  # lowest low over lookback period
        self.df['%R'] = -100 * (hh - self.df['Close']) / (hh - ll)

        # Plot graph
        fig = plt.figure()
        self.df['%R'].plot(lw=1.2, color='blue', label='Williams %R')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['%R'] < -80, 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['%R'] > -20, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
