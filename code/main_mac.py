import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.moving_average_crossover import MovingAverageCrossover
from backtest import Backtest
from evaluate import SharpeRatio, MaxDropdown, CAGR

# load data
df = pd.read_csv('../database/nasdaq_ticks_day/nasdaq_AAPL.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2015-01-01'):pd.Timestamp('2019-12-31')]

ticker = "AAPL"

# Moving average crossover

MAC = MovingAverageCrossover(df)
signals = MAC.gen_signals()
signal_fig = MAC.plot_signals()
signal_fig.suptitle('Moving average crossover - Signals', fontsize=14)
signal_fig.savefig('./figure/01-moving-average-crossover_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)

backtest_fig.suptitle('Moving average crossover - Portfolio value', fontsize=14)
backtest_fig.savefig('./figure/01-moving-average-crossover_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum dropdown
maxDropdown_fig = MaxDropdown(df)
maxDropdown_fig.suptitle('Moving average crossover - Maximum dropdown', fontsize=14)
maxDropdown_fig.savefig('./figure/01-moving-average-crossover_maximum-dropdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(df)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))