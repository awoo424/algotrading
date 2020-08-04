import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.cci_overbought_oversold import cciOverboughtOversold
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2019-12-31')]

ticker = "0005.HK"

# Moving average crossover

CCI_obos = cciOverboughtOversold(df)
signals = CCI_obos.gen_signals()
signal_fig = CCI_obos.plot_signals()
signal_fig.suptitle('CCI overbought & oversold - Signals', fontsize=14)
signal_fig.savefig('./figure/03-cci-overbought-oversold_signals')
plt.show()

cci_fig = CCI_obos.plot_CCI()
cci_fig.suptitle('CCI overbought & oversold - CCI', fontsize=14)
cci_fig.savefig('./figure/03-cci-overbought-oversold_cci')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('CCI overbought & oversold - Portfolio value', fontsize=14)
backtest_fig.savefig('./figure/03-cci-overbought-oversold_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDropdown_fig = MaxDrawdown(df)
maxDropdown_fig.suptitle('CCI overbought & oversold - Maximum dropdown', fontsize=14)
maxDropdown_fig.savefig('./figure/03-cci-overbought-oversold_maximum-dropdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))