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
# to-type

# sentiment analysis
from sentiment_analysis import sentiment_filter

"""
Technical analysis
-
Generate signals with MACD crossover strategy
"""

# load price data
df_whole = pd.read_csv('../../database/hkex_ticks_day/hkex_0005.csv', header=0, index_col='Date', parse_dates=True)

# select time range (for trading)
start_date = pd.Timestamp('2021-01-01')
end_date = pd.Timestamp('2021-02-05')
df = df_whole.loc[start_date:end_date]

# get filtered df for macro analysis
filtered_df = df_whole.loc[:start_date]

ticker = "0005.HK"

# apply MACD crossover strategy
macd_cross = macdCrossover(df)
macd_fig = macd_cross.plot_MACD()
#plt.close() # hide figure

signals = macd_cross.gen_signals()
signal_fig = macd_cross.plot_signals(signals)
#plt.close()

"""
Macroecnomic analysis
-
Adjust trading quantity with macroeconomic data
"""

# s_gdp, s_unemploy, s_property = get_sensitivity(filtered_df)

# traverse signals dataframe
## gdp, unemploy, property = get_macrodata(date)
## adj_factor = s_gdp * gdp + s_unemploy * unemploy s_property * property

# signals['signal'] = signals['signal] * adj_factor


"""
Sentiment analysis
- 
Filter out signals that contrats with the sentiment label
"""
filtered_signals = sentiment_filter(ticker, signals)

#print(len(filtered_signals))
#print(len(signals))

####### BELOW - code for reference #######

#print(df)
# Backtesting
portfolio, backtest_fig = Backtest(ticker, filtered_signals, df)
print("Final total value: {value:.4f} ".format(value=portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value=(
    portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]*100))
# for analysis
print("No. of trade: {value}".format(
    value=len(signals[signals.positions == 1])))

"""
portfolio, backtest_fig = Backtest(ticker, signals, df)
print("Final total value: {value:.4f} ".format(value = portfolio['total'][-1]))
print("Total return: {value:.4f}%".format(value = (portfolio['total'][-1] - portfolio['total'][0])/portfolio['total'][-1]*100))
# for analysis
print("No. of trade: {value}".format(value = len(signals[signals.positions == 1])))

backtest_fig.suptitle('MACD crossovers - Portfolio value', fontsize=14)
backtest_fig.savefig('./figures/macd-crossover_portfolio-value')
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
"""
