import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.relative_strength_index import rsi
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-10-01'):pd.Timestamp('2019-04-01')]

ticker = "0005.HK"

# RSI

rsi = rsi(df)
rsi_fig = rsi.plot_RSI()
rsi_fig.suptitle('HK.0005 - RSI', fontsize=14)
rsi_fig.savefig('./figures/05-rsi-plot')
plt.show()

signals = rsi.gen_signals()
signal_fig = rsi.plot_signals(signals)
signal_fig.suptitle('RSI - Signals', fontsize=14)
signal_fig.savefig('./figures/05-rsi_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final portfolio value (including cash): {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('RSI - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/05-rsi_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig = MaxDrawdown(df)
maxDrawdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/05-rsi_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))