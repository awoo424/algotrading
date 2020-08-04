import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.cci_emerging_trends import cciEmergingTrends
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2019-12-31')]

ticker = "0005.HK"
title = "{ticker} - CCI".format(ticker=ticker)

# CCI emerging trends

CCI_et = cciEmergingTrends(df)

signals = CCI_et.gen_signals()
signal_fig = CCI_et.plot_signals()
signal_fig.suptitle('CCI emerging trends - Signals', fontsize=14)
signal_fig.savefig('./figures/02-cci-emerging-trends_signals')
plt.show()

cci_fig = CCI_et.plot_CCI()
cci_fig.suptitle(title, fontsize=14)
cci_fig.savefig('./figures/02-cci-emerging-trends_cci')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('CCI emerging trends - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/02-cci-emerging-trends_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDropdown_fig = MaxDrawdown(df)
maxDropdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDropdown_fig.savefig('./figures/02-cci-emerging-trends_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))