import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.macd_crossover import macdCrossover
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-10-01'):pd.Timestamp('2019-04-01')]

ticker = "0005.HK"

# MACD

macd_cross = macdCrossover(df)
macd_fig = macd_cross.plot_MACD()
macd_fig.suptitle('HK.0005 - MACD', fontsize=14)
macd_fig.savefig('./figures/04-macd-plot')
plt.show()

signals = macd_cross.gen_signals()
signal_fig = macd_cross.plot_signals()
signal_fig.suptitle('MACD crossovers - Signals', fontsize=14)
signal_fig.savefig('./figures/04-macd-crossovers_signals')
plt.show()

signal_fig = macd_cross.plot_signals_MACD()
signal_fig.suptitle('MACD crossovers - Signals (Verify)', fontsize=14)
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('MACD crossovers - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/04-macd-crossovers_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDropdown_fig = MaxDrawdown(df)
maxDropdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDropdown_fig.savefig('./figures/04-macd-crossovers_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))