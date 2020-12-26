import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.volume_roc import volume_roc
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# Volume Rate of Change

vroc = volume_roc(df)
vroc_fig = vroc.plot_VROC()
vroc_fig.suptitle('HK.0005 - Volume ROC', fontsize=14)
vroc_fig.savefig('./figures/volume/03-volume-rate-of-change-plot')
plt.show()

signals = vroc.gen_signals()
signal_fig = vroc.plot_signals(signals)
signal_fig.suptitle('Volume ROC - Signals', fontsize=14)
signal_fig.savefig('./figures/volume/03-volume-rate-of-change_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final portfolio value (including cash): {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('Volume ROC - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/volume/03-volume-rate-of-change_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('True Strength Index (TSI) - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/volume/03-volume-rate-of-change_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
