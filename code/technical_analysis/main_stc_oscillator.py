import sys
sys.path.append("..")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from strategy.stochastic_oscillator import stc_oscillator
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2020-01-01')]

ticker = "0005.HK"

# Stochastic Oscillator

stc = stc_oscillator(df)
stc_fig = stc.plot_KD()
stc_fig.suptitle('HK.0005 - %K and %D lines', fontsize=14)
stc_fig.savefig('./figures/momentum/05-stc-oscillator_kd-lines')
plt.show()


signals = stc.gen_signals()
signal_fig = stc.plot_signals(signals)
signal_fig.suptitle('Stochastic Oscillator - Signals', fontsize=14)
signal_fig.savefig('./figures/momentum/05-stc-oscillator_signals')
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final portfolio value (including cash): {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}".format(value = portfolio['total'][-1] - portfolio['total'][0]))

backtest_fig.suptitle('RSI - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/momentum/05-stc-oscillator_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig = MaxDrawdown(df)
maxDrawdown_fig.suptitle('CCI emerging trends - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/momentum/05-stc-oscillator_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))