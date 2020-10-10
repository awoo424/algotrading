import sys
sys.path.append("..")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.bollinger_bands import bollinger_bands
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# Bollinger Bands

bb = bollinger_bands(df)
bb_fig = bb.plot_BB()
bb_fig.suptitle('HK.0005 - Bollinger Bands', fontsize=14)
bb_fig.savefig('./figures/volatility/01-bollinger-bands-plot')
plt.show()


signals = bb.gen_signals()
signal_fig = bb.plot_signals(signals)
signal_fig.suptitle('Bollinger Bands - Signals', fontsize=14)
signal_fig.savefig('./figures/volatility/01-bollinger-bands_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final portfolio value (including cash): {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('Bollinger Bands - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/volatility/01-bollinger-bands_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig = MaxDrawdown(df)
maxDrawdown_fig.suptitle('Bollinger Bands - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/volatility/01-bollinger-bands_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))