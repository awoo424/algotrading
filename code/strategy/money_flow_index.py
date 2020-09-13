from .indicator import Indicator
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Money Flow Index (MFI)
-
Buy when MFI crosses the upper threshold, (oversold)
sell when MFI crosses the lower threshold. (overbought)
"""


class mfi(Indicator):
    def __init__(self, df, n=14):
        super().__init__(df)
        self.df = df
        self.n = n
        self.lower = 20 # usually levels of 10-90
        self.upper = 80

    """
    Formula
    -
    Money Flow Index = 100 - 100 / (1 + Money Flow Ratio)

    Raw Money Flow = Typical Price x Volume
    Typical Price = (High + Low + Close) / 3
    Money Flow Ratio = (14-period Positive Money Flow) / (14-period Negative Money Flow)
    """

    def plot_MFI(self):
        # Typical price
        tp = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3.0

        # positive = 1, negative = -1
        self.df['Sign'] = np.where(tp > tp.shift(
            1), 1, np.where(tp < tp.shift(1), -1, 0))

        # Money flow
        self.df['Money flow'] = tp * self.df['Volume'] * self.df['Sign']

        # 4 positive and negative money flow with n periods
        n_positive_mf = self.df['Money flow'].rolling(
            self.n).apply(lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True)
        n_negative_mf = abs(
            self.df['Money flow'].rolling(self.n).apply(lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True))

        # Money flow index
        mf_ratio = n_positive_mf / n_negative_mf
        self.df['MFI'] = (100 - (100 / (1 + mf_ratio)))

        # Plot graph
        fig = plt.figure()
        self.df['MFI'].plot(lw=1.2, label='Money Flow Index (MFI)')
        plt.legend()

        return fig

    def gen_signals(self):
        # Initialize the `signals` DataFrame with the `signal` column
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['MFI'] > self.upper, 'signal'] = 1.0

        # Generate sell signal
        signals.loc[self.df['MFI'] < self.lower, 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        # signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        # signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals
