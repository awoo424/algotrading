import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.stochastic_oscillator import stc_oscillator
from backtest import Backtest
from evaluate import SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2019-01-01')]

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
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value = (portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]*100))
# for analysis
print("No. of trade: {value}".format(value = len(signals[signals.positions == 1])))

backtest_fig.suptitle('STC Oscillator - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/momentum/05-stc-oscillator_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 2. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('STC Oscillator - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/momentum/05-stc-oscillator_maximum-drawdown')
plt.show()

# 3. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
