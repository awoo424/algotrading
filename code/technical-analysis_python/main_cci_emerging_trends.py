import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.cci_emerging_trends import cciEmergingTrends
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/microeconomic_data/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"
title = "{ticker} - CCI".format(ticker=ticker)

# CCI emerging trends

CCI_et = cciEmergingTrends(df)

signals = CCI_et.gen_signals()
signal_fig = CCI_et.plot_signals(signals)
signal_fig.suptitle('CCI emerging trends - Signals', fontsize=14)
signal_fig.savefig('./figures/momentum/01-cci-emerging-trends_signals')
plt.show()

cci_fig = CCI_et.plot_CCI()
cci_fig.suptitle(title, fontsize=14)
cci_fig.savefig('./figures/momentum/01-cci-emerging-trends_cci')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))
print("Average daily return: {value:.4f}%".format(value = portfolio['returns'].mean()*100))

backtest_fig.suptitle('CCI emerging trends - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/momentum/01-cci-emerging-trends_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/momentum/01-cci-emerging-trends_maximum-drawdown')
plt.show()

maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
