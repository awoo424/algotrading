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


def backtest(symbol):
    price_file = '../../database/microeconomic_data/hkex_ticks_day/hkex_' + symbol + '.csv'

    # load price data
    df_whole = pd.read_csv(price_file, header=0, index_col='Date', parse_dates=True)

    # select time range (for trading)
    #start = '2017-01-03'
    start = '2020-06-10'
    end = '2021-03-03'
    start_date = pd.Timestamp(start)
    end_date = pd.Timestamp(end)

    df = df_whole.loc[start_date:end_date]

    ticker = symbol + ".HK"

    # load signals csv (output from ML model)
    signals_file = './LSTM_price-only_output/' + symbol + '_output.csv'

    signals = pd.read_csv(signals_file,
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
    backtest_fig.suptitle('Portfolio value', fontsize=14)
    #backtest_fig.savefig('./figures_LSTM-price-only/' + symbol + '-portfolio-value')
    #plt.show()

    # Evaluate strategy

    # 1. Portfolio return
    returns_fig = PortfolioReturn(portfolio)
    returns_fig.suptitle('Portfolio return')
    #returns_filename = './figures_LSTM-price-only/' + symbol + '-portfolo-return'
    #returns_fig.savefig(returns_filename)
    #plt.show()

    # 2. Sharpe ratio
    sharpe_ratio = SharpeRatio(portfolio)
    print("Sharpe ratio: {ratio:.4f} ".format(ratio=sharpe_ratio))

    # 3. Maximum drawdown
    maxDrawdown_fig, max_daily_drawdown, daily_drawdown = MaxDrawdown(df)
    maxDrawdown_fig.suptitle('Baseline - Maximum drawdown', fontsize=14)
    #maxDrawdown_filename = './figures/' + symbol + '-LSTM_maximum-drawdown'
    #maxDrawdown_fig.savefig(maxDrawdown_filename)
    #plt.show()

    # 4. Compound Annual Growth Rate
    cagr = CAGR(portfolio)
    print("CAGR: {cagr:.4f} ".format(cagr=cagr))


    # Write to file
    f = open("LSTM_price-only_results.csv", "a")
    f.write(ticker + ',' + start + ',' + end + ',' + str(portfolio_return) + ',' +
            str(sharpe_ratio) + ',' + str(cagr) + ',' + str(trade_signals_num) + '\n')
    f.close()

def main():
    ticker_list = ['0001', '0002', '0003', '0004', '0005', '0016', '0019', '0168', '0175', '0386', '0388', '0669', '0700',
                   '0762', '0823', '0857', '0868', '0883', '0939', '0941', '0968', '1211', '1299', '1818', '2319', '2382', '2688', '2689', '2899']

    #ticker_list = ['0001', '0002', '0003', '0004', '0005']

    for ticker in ticker_list:

        print("############ Ticker: " + ticker + " ############")
        backtest(ticker)
        print('\n')

if __name__ == "__main__":
    main()
