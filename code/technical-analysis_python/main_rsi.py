import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.relative_strength_index import rsi
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/microeconomic_data/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2019-01-01')]

ticker = "0005.HK"

# RSI

rsi = rsi(df)
rsi_fig = rsi.plot_RSI()
rsi_fig.suptitle('HK.0005 - RSI', fontsize=14)
rsi_fig.savefig('./figures/momentum/03-rsi-plot')
plt.show()

signals = rsi.gen_signals()
signal_fig = rsi.plot_signals(signals)
signal_fig.suptitle('RSI - Signals', fontsize=14)
signal_fig.savefig('./figures/momentum/03-rsi_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value = (portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][0]*100))
# for analysis
print("No. of trade: {value}".format(value = len(signals[signals.positions == 1])))

backtest_fig.suptitle('RSI - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/momentum/03-rsi_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/momentum/03-rsi_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
