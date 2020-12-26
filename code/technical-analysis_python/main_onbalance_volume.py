import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.onbalance_volume import obv
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# On-Balance Volume

obv = obv(df)
obv_fig = obv.plot_OBV()
obv_fig.suptitle('HK.0005 - On-Balance Volume', fontsize=14)
obv_fig.savefig('./figures/volume/02-onbalance-volume-plot')
plt.show()
