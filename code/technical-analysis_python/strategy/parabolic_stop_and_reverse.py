from .indicator import Indicator 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Parabolic Stop and Reverse (Parabolic SAR)
-
Buy if falling SAR goes below the price, (bullish signal)
sell if rising SAR goes above the price. (bearish signal)

:initial_af: initial acceleration factor
:max_af: maximum acceleration factor  

Code ref: https://virtualizedfrog.wordpress.com/2014/12/09/parabolic-sar-implementation-in-python/
"""
class ParabolicSAR(Indicator):
    def __init__(self, df, initial_af=0.02, max_af=0.2):
        super().__init__(df)
        self.df = df
        self.initial_af = initial_af
        self.max_af = max_af

    """
    Formula
    -
    1. Rising SAR (Uptrend)

    Current SAR = Prior SAR + Prior AF * (Prior EP - Prior SAR)

    Prior SAR: The SAR value for previous period. 
    Extreme Point (EP): The highest high of the current uptrend. 
    Acceleration Factor (AF): Starting at 0.02, increases by 0.02 each time the extreme point 
    makes a new high. AF can only reach a maximum of 0.2, no matter how long the uptrend extends. 

    Note that SAR can never be above the prior two periods' lows. Should SAR be 
    above one of those lows, use the lowest of the two for SAR. 
    ---------------------------

    2. Falling SAR (Downtrend)

    Current SAR = Prior SAR + Prior AF * (Prior EP - Prior SAR)

    Prior SAR: The SAR value for previous period. 
    Extreme Point (EP): The lowest low of the current downtrend. 
    Acceleration Factor (AF): Starting at 0.02, increases by 0.02 each time the extreme point 
    makes a new low. AF can only reach a maximum of 0.2, no matter how long the downtrend extends.

    Note that SAR can never be below the prior two periods' highs. Should SAR be 
    below one of those highs, use the highest of the two for SAR. 
    """
    def plot_PSAR(self):
        length = len(self.df)
        array_dates = list(self.df.index)
        array_high = list(self.df['High'])
        array_low = list(self.df['Low'])
        array_close = list(self.df['Close'])

        psar = self.df['Close'].copy()
        psarbull = [None] * len(self.df)
        psarbear = [None] * len(self.df)
        
        bull = True
        af = self.initial_af # initialise acceleration factor

        if length > 0:
            ep = array_low[0] # extreme price
            hp = array_high[0] # extreme high
            lp = array_low[0] # extreme low

        for i in range(2, len(self.df)):
            if bull:
                # Rising SAR
                psar[i] = psar[i-1] + af * (hp - psar[i-1])
            else:
                # Falling SAR
                psar[i] = psar[i-1] + af * (lp - psar[i-1])

            reverse = False

            # Check reversion point
            if bull:
                if array_low[i] < psar[i]:
                    bull = False
                    reverse = True
                    psar[i] = hp
                    lp = array_low[i]
                    af = self.initial_af
            else:
                if array_high[i] > psar[i]:
                    bull = True
                    reverse = True
                    psar[i] = lp
                    hp = array_high[i]
                    af = self.initial_af

            if not reverse:
                if bull:
                    # Extreme high makes a new high
                    if array_high[i] > hp:
                        hp = array_high[i]
                        af = min(af + self.initial_af, self.max_af)

                    # Check if SAR goes abov prior two periods' lows. 
                    # If so, use the lowest of the two for SAR.
                    if array_low[i-1] < psar[i]:
                        psar[i] = array_low[i-1]
                    if array_low[i-2] < psar[i]:
                        psar[i] = array_low[i-2]

                else:
                    # Extreme low makes a new low
                    if array_low[i] < lp:
                        lp = array_low[i]
                        af = min(af + self.initial_af, self.max_af)

                    # Check if SAR goes below prior two periods' highs. 
                    # If so, use the highest of the two for SAR.
                    if array_high[i-1] > psar[i]:
                        psar[i] = array_high[i-1]
                    if array_high[i-2] > psar[i]:
                        psar[i] = array_high[i-2]

            # Save rising SAR
            if bull:
                psarbull[i] = psar[i]
            # Save falling SAR
            else:
                psarbear[i] = psar[i]

        self.df['psar'] = psar
        self.df['psarbull'] = psarbull
        self.df['psarbear'] = psarbear

        # Plot graph
        fig = plt.figure()

        self.df['Close'].plot(lw=0.8, color='black', label='Closing price')

        if (self.df['psarbull'].size > 0):
            self.df['psarbull'].plot(lw=1.2, color='green', label='Rising SAR')

        if (self.df['psarbear'].size > 0):
            self.df['psarbear'] = self.df['psarbear'].astype(float)
            self.df['psarbear'].plot(lw=1.2, color='red', label='Falling SAR')

        plt.legend()

        return fig

    def gen_signals(self):
        signals = pd.DataFrame(index=self.df.index)
        signals['signal'] = 0.0

        # Generate buy signal
        signals.loc[self.df['psarbull'].notnull(), 'signal'] = 1.0
        
        # Generate sell signal
        signals.loc[self.df['psarbear'].notnull(), 'signal'] = -1.0

        # Generate trading order
        signals['positions'] = signals['signal'].diff()
        signals.loc[signals['positions'] > 0, 'positions'] = 1.0
        signals.loc[signals['positions'] < 0, 'positions'] = -1.0

        self.signals = signals

        return signals