import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys
sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

import matplotlib.pyplot as plt
from strategy.macd_crossover import macdCrossover
from backtest import Backtest
from evaluate import PortfolioReturn, SharpeRatio, MaxDrawdown, CAGR

# load data
df = pd.read_csv('../../database/microeconomic_data/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range
df = df.loc[pd.Timestamp('2017-01-01'):pd.Timestamp('2021-01-01')]

ticker = "0005.HK"

# MACD

macd_cross = macdCrossover(df)
macd_fig = macd_cross.plot_MACD()
macd_fig.suptitle('HK.0005 - MACD', fontsize=14)
macd_fig.savefig('./figures/trend/02-macd-plot')
plt.show()

signals = macd_cross.gen_signals()
signal_fig = macd_cross.plot_signals(signals)
signal_fig.suptitle('MACD crossovers - Signals', fontsize=14)
signal_fig.savefig('./figures/trend/02-macd-crossover_signals')
plt.show()

signal_fig = macd_cross.plot_signals_MACD()
signal_fig.suptitle('MACD crossovers - Signals', fontsize=14)
plt.show()

# Backtesting

portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value = (portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]*100))
# for analysis
print("No. of trade: {value}".format(value = len(signals[signals.positions == 1])))

backtest_fig.suptitle('MACD crossovers - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/trend/02-macd-crossover_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Portfolio return
returns_fig = PortfolioReturn(portfolio)
returns_fig.suptitle('MACD crossovers - Portfolio return')
returns_fig.savefig('./figures/trend/02-macd-crossover_portfolo-return')
plt.show()

# 2. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 3. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('MACD crossovers - Maximum drawdown', fontsize=14)
maxDrawdown_fig.savefig('./figures/trend/02-macd-crossover_maximum-drawdown')
plt.show()

# 4. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))
