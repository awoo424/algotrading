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

# macroeconomic analysis
from filters.macro_analysis import GetSensitivity, GetMacrodata

# sentiment analysis
from filters.sentiment_analysis import SentimentFilter

"""
Technical analysis
-
Generate signals with MACD crossover strategy
"""

# load price data
df_whole = pd.read_csv('../../database/microeconomic_data/hkex_ticks_day/hkex_0001.csv', header=0, index_col='Date', parse_dates=True)

# select time range (for trading)
start_date = pd.Timestamp('2017-01-01')
end_date = pd.Timestamp('2021-01-01')
#start_date = pd.Timestamp('2017-01-01')
#end_date = pd.Timestamp('2019-02-05')
df = df_whole.loc[start_date:end_date]

# get filtered df for macro analysis
filtered_df = df_whole.loc[:end_date]

ticker = "0005.HK"

# apply MACD crossover strategy
macd_cross = macdCrossover(df)
macd_fig = macd_cross.plot_MACD()
plt.close() # hide figure

signals = macd_cross.gen_signals()
print(signals.head())
signal_fig = macd_cross.plot_signals(signals)
plt.close()  # hide figure

"""
Macroecnomic analysis
-
Adjust bias in signals with macroeconomic data
"""
# get ticker's sensitivity to macro data
s_gdp, s_unemploy, s_property = GetSensitivity(filtered_df)

# append signals with macro data
signals = GetMacrodata(signals)

# calculate adjusting factor
signals['macro_factor'] = s_gdp * signals['GDP'] + s_unemploy * signals['Unemployment rate'] + s_property * signals['Property price']
signals['signal'] = signals['signal'] + signals['macro_factor']

# round off signals['signal'] to the nearest integer
signals['signal'] = signals['signal'].round(0)

"""
Sentiment analysis
- 
Filter out signals that contrast with the sentiment label
"""
filtered_signals = SentimentFilter(ticker, signals)

"""
Backtesting & evaluation
"""
portfolio, backtest_fig = Backtest(ticker, filtered_signals, df)
plt.close() # hide figure
print("Final total value: {value:.4f} ".format(value=portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value=(((portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]) * 100))) # for analysis
print("No. of trade: {value}".format(value=len(signals[signals.positions == 1])))


"""
Plotting figures
"""
backtest_fig.suptitle('Baseline - Portfolio value', fontsize=14)
#backtest_fig.savefig('./figures/baseline_portfolio-value')
plt.show()

# Evaluate strategy

# 1. Portfolio return
returns_fig = PortfolioReturn(portfolio)
returns_fig.suptitle('Baseline - Portfolio return')
#returns_fig.savefig('./figures/baseline_portfolo-return')
plt.show()

# 2. Sharpe ratio
sharpe_ratio = SharpeRatio(portfolio)
print("Sharpe ratio: {ratio:.4f} ".format(ratio = sharpe_ratio))

# 3. Maximum drawdown
maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
maxDrawdown_fig.suptitle('Baseline - Maximum drawdown', fontsize=14)
#maxDrawdown_fig.savefig('./figures/baseline_maximum-drawdown')
plt.show()

# 4. Compound Annual Growth Rate
cagr = CAGR(portfolio)
print("CAGR: {cagr:.4f} ".format(cagr = cagr))

