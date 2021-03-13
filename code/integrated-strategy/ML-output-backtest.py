import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys

sys.path.append("..")
sys.path.append("../technical-analysis_python/")
mpl.use('tkagg')  # issues with Big Sur

# technical analysis
from strategy.macd_crossover import macdCrossover
from backtest import Backtest
from evaluate import PortfolioReturn, SharpeRatio, MaxDrawdown, CAGR

# load price data
df_whole = pd.read_csv('../../database/microeconomic_data/hkex_ticks_day/hkex_0001.csv',
                       header=0, index_col='Date', parse_dates=True)

# select time range (for trading)
start = '2017-01-03'
end = '2020-09-30'
start_date = pd.Timestamp(start)
end_date = pd.Timestamp(end)

df = df_whole.loc[start_date:end_date]

ticker = "0001.HK"
symbol = "0001"

# load signals csv (output from ML model)
signals = pd.read_csv('0001_output.csv',
                      header=0, index_col='Date', parse_dates=True)
signals['positions'] = signals['signal'].diff()
signals = signals[~signals.index.duplicated(keep='first')]

df = df[~df.index.duplicated(keep='first')]
#print(signals.head())
#print(df.head())

"""
Backtesting & evaluation
"""
portfolio, backtest_fig = Backtest(ticker, signals, df)
plt.close()  # hide figure
print("Final total value: {value:.4f} ".format(
        value=portfolio['total'][-1]))

portfolio_return = (
    ((portfolio['total'][-1] - portfolio['total'][0]) / portfolio['total'][-1]) * 100)
print("Total return: {value:.4f}%".format(value=portfolio_return))

trade_signals_num = len(signals[signals.positions == 1])
print("No. of trade: {value}".format(
    value=trade_signals_num))


"""
Plotting figures
"""
backtest_fig.suptitle('Baseline - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/' + symbol + '-LSTM_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Portfolio return
returns_fig = PortfolioReturn(portfolio)
returns_fig.suptitle('Baseline - Portfolio return')
returns_filename = './figures/' + symbol + '-LSTM_portfolo-return'
returns_fig.savefig(returns_filename)
#plt.show()

# 2. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio=sharpe_ratio))

# 3. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('Baseline - Maximum drawdown', fontsize=14)
maxDrawdown_filename = './figures/' + symbol + '-LSTM_maximum-drawdown'
maxDrawdown_fig.savefig(maxDrawdown_filename)
#plt.show()

# 4. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr=cagr))


# Write to file
f = open("LSTM_results.csv", "a")
f.write(ticker + ',' + start + ',' + end + ',' + str(portfolio_return) + ',' +
        str(sharpe_ratio) + ',' + str(cagr) + ',' + str(trade_signals_num) + '\n')
f.close()
