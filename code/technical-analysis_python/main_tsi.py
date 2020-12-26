import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.true_strength_index import tsi
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# True Strength Index

tsi = tsi(df)
tsi_fig = tsi.plot_TSI()
tsi_fig.suptitle('HK.0005 - TSI & Signal line', fontsize=14)
tsi_fig.savefig('./figures/momentum/06-tsi-plot')
plt.show()

signals = tsi.gen_signals()
signal_fig = tsi.plot_signals(signals)
signal_fig.suptitle('True Strength Index (TSI) - Signals', fontsize=14)
signal_fig.savefig('./figures/momentum/06-tsi_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final portfolio value (including cash): {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('TSI - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/momentum/06-tsi_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('True Strength Index (TSI) - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/momentum/06-tsi_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
