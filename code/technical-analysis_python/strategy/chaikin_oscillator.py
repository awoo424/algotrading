from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Chaikin Oscillator
-
Buy when the oscillator is positive,
sell when the oscillator is negative.
"""

class co(Indicator):
    def __init__(self, df, short_w=3, long_w=10):
        super().__init__(df)
        self.df = df
        self.short_w = short_w # window size for shorter period
        self.long_w = long_w # window size of longer period

    """
    Formula
    -
    Chaikin Oscillator = (3-day EMA of ADL)  -  (10-day EMA of ADL)

    Accumulation Distribution Line (ADL)
    -------------------------------------
    ADL = Previous ADL + Current Period's Money Flow Volume

    Money Flow Volume = Money Flow Multiplier x Volume for the Period
    Money Flow Multiplier = [(Close - Low) - (High - Close)] / (High - Low) 
   
    """

    def plot_CO(self):
        # Compute money flow multiplier
        self.df['MFM'] = ((self.df['Close'] - self.df['Low']) - self.df['High'] - self.df['Close']) / (self.df['High'] - self.df['Low'])
        # Compute money flow volume
        self.df['MFV'] = self.df['MFM'] * self.df['Volume']
        # Compute ADL
        # adl = [None] * len(self.df)
        # for i in range (1,len(self.df)):
        #     adl[i] = adl[i-1] + mfm[i]
        self.df['ADL'] = self.df['Close'].shift(1) + self.df['MFV']

        ema_long = self.df['ADL'].ewm(ignore_na=False, min_periods=0, com=self.short_w, adjust=True).mean()
        ema_short = self.df['ADL'].ewm(ignore_na=False, min_periods=0, com=self.long_w, adjust=True).mean()
        self.df['Chaikin'] = ema_short - ema_long

        # Plot graph
        fig = plt.figure()
        self.df['Chaikin'].plot(lw=1.2, color='blue', label='Chaikin Oscillator')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['Chaikin'] > 0, 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['Chaikin'] < 0, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
