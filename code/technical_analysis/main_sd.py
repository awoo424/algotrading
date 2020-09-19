import sys
sys.path.append("..")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.standard_deviation import sd
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# Standard Deviation

sd = sd(df)

sd_result = sd.cal_SD()
print(sd_result)

sd_fig = sd.plot_SD()
sd_fig.suptitle('HK.0005 - Standard Deviation', fontsize=14)
sd_fig.savefig('./figures/volatility/03-standard-deviation-plot')
plt.show()