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
from macro_analysis import GetSensitivity, GetMacrodata

# sentiment analysis
from sentiment_analysis import SentimentFilter


def baseline_strategy(symbol, start, end):
    """
    Technical analysis
    -
    Generate signals with MACD crossover strategy
    """
    # import pathlib
    # print(pathlib.Path(__file__).parent.absolute())

    filename = "../../database/microeconomic_data/hkex_ticks_day/hkex_" + symbol + ".csv"

    # load price data
    df_whole = pd.read_csv(
        filename, header=0, index_col='Date', parse_dates=True)

    # select time range (for trading)
    start_date = pd.Timestamp(start)
    end_date = pd.Timestamp(end)

    df = df_whole.loc[start_date:end_date]

    # get filtered df for macro analysis
    filtered_df = df_whole.loc[:end_date]

    ticker = symbol + ".HK"

    # apply MACD crossover strategy
    macd_cross = macdCrossover(df)
    macd_fig = macd_cross.plot_MACD()
    plt.close()  # hide figure

    signals = macd_cross.gen_signals()
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
    signals['macro_factor'] = s_gdp * signals['GDP'] + s_unemploy * \
        signals['Unemployment rate'] + s_property * signals['Property price']
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
    print("############ Ticker: " + ticker + " ############")

    portfolio, backtest_fig = Backtest(ticker, filtered_signals, df)
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
    backtest_filename = "./figures/" + symbol + "-baseline_portfolio-value"
    backtest_fig.savefig(backtest_filename)
    #plt.show()

    # Evaluate strategy

    # 1. Portfolio return
    returns_fig = PortfolioReturn(portfolio)
    returns_fig.suptitle('Baseline - Portfolio return')
    returns_filename = './figures/' + symbol + '-baseline_portfolo-return'
    returns_fig.savefig(returns_filename)
    #plt.show()

    # 2. Sharpe ratio
    sharpe_ratio = SharpeRatio(portfolio)
    print("Sharpe ratio: {ratio:.4f} ".format(ratio=sharpe_ratio))

    # 3. Maximum drawdown
    maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
    maxDrawdown_fig.suptitle('Baseline - Maximum drawdown', fontsize=14)
    maxDrawdown_filename = './figures/' + symbol + '-baseline_maximum-drawdown'
    maxDrawdown_fig.savefig(maxDrawdown_filename)
    #plt.show()

    # 4. Compound Annual Growth Rate
    cagr = CAGR(portfolio)
    print("CAGR: {cagr:.4f} ".format(cagr=cagr))

    # Write to output file
    f = open("baseline_results.csv", "a")
    f.write(ticker + ',' + start + ',' + end + ',' + str(portfolio_return) + ',' +
            str(sharpe_ratio) + ',' + str(cagr) + ',' + str(trade_signals_num) + '\n')
    f.close()


def main():
    ticker_list = ['0001', '0002', '0003', '0004', '0005', '0016', '0019', '0113', '0168', '0175', '0386', '0388', '0669', '0700',
                   '0762', '0823', '0857', '0868', '0883', '0939', '0941', '0968', '1211', '1299', '1818', '2319', '2382', '2688', '2689', '2899']

    for ticker in ticker_list:
        start = '2017-01-01'
        end = '2021-01-01'
        baseline_strategy(ticker, start, end)


if __name__ == "__main__":
    main()
