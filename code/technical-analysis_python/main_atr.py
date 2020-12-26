import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt

from strategy.average_true_range import atr

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# True Strength Index

atr = atr(df)
atr.cal_ATR()
atr_fig = atr.plot_ATR()
atr_fig.suptitle('HK.0005 - Average True Range (ATR)', fontsize=14)
atr_fig.savefig('./figures/volatility/02-average-true-range-plot')
plt.show()

# Check if it is highly volatile

atr.cal_ATR(250)
volatile = atr.high_volatility()
print(volatile)
