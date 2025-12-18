Write a technical strategy
=====================================

.. highlight:: Julia

In this tutorial, you will learn to do the following in Julia:

* Write a trading strategy
* Backtest the strategy
* Plot the trading signals
* Evalaute strategy performance


You could run the code for this tutorial in :code:`code/technical-analysis_julia/moving_average.jl` 
or :code:`code/technical-analysis_julia/moving-average.ipynb`. 


You would need to install and import the following libraries:

::

  # import libraries
  using CSV;
  using Dates;
  using DataFrames;
  using Statistics;
  using Plots;
  using PyCall;
  using RollingFunctions;

  @pyimport matplotlib.pyplot as plt


First, load the file from the sample database:

::

  # load data
  df = CSV.File("../../database/microeconomic_data/hkex_ticks_day/hkex_0001.csv") |> DataFrame

  ticker = "0001.HK" # set this variable for plot title

Build the strategy
--------------------------

We will use Moving Average (MA) as the example here. You could refer to the section :any:`Moving Averages (MA)` 
to read the formulae and conditions for generating buy/sell signals.

Calculate the short and long moving averages, 
and respectively append them to the :code:`signals` dataframe:

::

  # initialise signals dataframe
  signals = df[:,[:Date, :Close]]

  dates = Array(convert(Matrix, select(df, :Date))) # get dates
  close = convert(Matrix, select(df, :Close)) # get closing price

  # short MA
  short_window = 40
  short_mavg = runmean(vec(close), short_window)
  insertcols!(signals, 1, :short_mavg => short_mavg)

  # long MA
  long_window = 100
  long_mavg = runmean(vec(close), long_window)
  insertcols!(signals, 1, :long_mavg => long_mavg)

Generate the buy and sell signals based on the :code:`short_mavg` and :code:`long_mavg` colums:

::

  # Create signals
  signal = Float64[]
          
  for i in 1:length(short_mavg)
      if short_mavg[i] > long_mavg[i]
          x = 1.0 # buy signal
      else
          x = 0.0
      end
      push!(signal, x)
  end

  insertcols!(signals, 1, :signal => signal)

Generate the positions by taking the row differences in :code:`signal`:

::

  # Generate positions
  function gen_pos(signal)
      positions = zeros(length(signal))
      positions[1] = 0
      for i in 2:length(signal)
          positions[i] = signal[i] - signal[i-1]
      end
      return positions
  end

  positions = gen_pos(signal)
  insertcols!(signals, 1, :positions => positions)

We also generate temporary arrays for plotting buy and sell signals respectively:

::

  # Generate tmp arrays to plot buy signals

  buy_signals = DataFrame()
  buy_dates = []
  buy_prices = []

  for i in 1:length(positions)
      if (positions[i] == 1.0)
        push!(buy_dates, dates[i])
        push!(buy_prices, close[i])
      end
  end

  insertcols!(buy_signals, 1, :Date => buy_dates)
  insertcols!(buy_signals, 1, :Price => buy_prices)
  #print(first(buy_signals,10))

  # Generate tmp arrays to plot sell signals

  sell_signals = DataFrame()
  sell_dates = []
  sell_prices = []

  for i in 1:length(positions)
      if (positions[i] == -1.0)
        push!(sell_dates, dates[i])
        push!(sell_prices, close[i])
      end
  end

  insertcols!(sell_signals, 1, :Date => sell_dates)
  insertcols!(sell_signals, 1, :Price => sell_prices)


Plotting graphs
----------------

As we make use of :code:`matplotlib` to plot graphs, the functions are very similar to those
we have used in Python.

::

  fig = plt.figure() # Initialise the plot figure
  ax1 = fig.add_subplot(111, ylabel="Price in \$") # Add a subplot and label for y-axis

  # plot moving averages as line
  plt.plot(signals.Date, signals.short_mavg, color="blue", linewidth=1.0, label="Short MA")
  plt.plot(signals.Date, signals.long_mavg, color="orange", linewidth=1.0, label="Long MA")

  # plot signals with colour markers
  plt.plot(buy_signals.Date, buy_signals.Price, marker=10, markersize=7, color="m", linestyle="None", label="Buy signal")
  plt.plot(sell_signals.Date, sell_signals.Price, marker=11, markersize=7, color="k", linestyle="None", label="Sell signal")

  plt.title("MA crossover signals")
  plt.show()

  # save fig
  fig.savefig("./figures/moving-average-crossover_signals", dpi=100)


Backtesting
------------

We could then backtest the strategy on the historical price data:

::

  initial_capital = 100000.0

  # Initialise the portfolio with value owned
  portfolio = signals[:,[:Date, :Close, :positions]]
  portfolio[:trade] = signals[:Close] .* (100 .* signals[:positions])

  # Add `holdings` to portfolio
  portfolio[:quantity] = cumsum(100 .* signals[:positions])
  portfolio[:holdings] = portfolio[:Close] .* portfolio[:quantity]

  # Add `cash` to portfolio
  portfolio[:cash] = initial_capital .- cumsum(portfolio[:trade])

  # Add `total` to portfolio
  portfolio[:total] = portfolio[:cash] .+ portfolio[:holdings]

  portfolio_total = Array(portfolio[:total])

  # Generate returns
  function gen_returns(portfolio_total)
      returns = zeros(length(portfolio_total))
      returns[1] = 0
      for i in 2:length(portfolio_total)
          returns[i] = (portfolio_total[i] - portfolio_total[i-1]) / portfolio_total[i-1]
      end
      return returns
  end

  returns = gen_returns(portfolio_total)
  insertcols!(portfolio, 1, :returns => returns)

  # Print final portfolio value and total return in terminal

  @printf("Final total value: %f\n", portfolio.total[size(portfolio,1)])

  total_return = (portfolio.total[size(portfolio,1)] - portfolio.total[1]) / portfolio.total[1]
  @printf("Total return: %f\n", total_return)

Strategy evaluation
--------------------

Note that all the evalation metric functions are designed to take the portfolio dataframe
as argument. You could refer to the :any:`Evaluation metrics` section the mathematical formulae for each evaluation metric.

Portfolio return
""""""""""""""""""
::

  function portfolio_return(portfolio)
  fig = plt.figure() # Initialise the plot figure
  ax1 = fig.add_subplot(111, ylabel="Total in \$") # Add a subplot and label for y-axis

  plt.plot(portfolio.Date, portfolio.returns, color="blue", linewidth=1.0, label="Returns")

  plt.title("MA crossover portfolio return")
  plt.show()

  # save fig
  fig.savefig("./figures/moving-average-crossover_returns", dpi=100)
  end

::

  # call function
  portfolio_return(portfolio)

Sharpe ratio
"""""""""""""""
::

  function sharpe_ratio(portfolio)
  # Annualised Sharpe ratio
  sharpe_ratio = sqrt(252) * (mean(returns) / std(returns))

  return sharpe_ratio
  end

::

  # Call function and print output
  sharpe = sharpe_ratio(portfolio)
  @printf("Sharpe ratio: %f\n", sharpe)


Compound Annual Growth Rate (CAGR)
""""""""""""""""""""""""""""""""""""""

::

  function CAGR(portfolio)
  # Get the number of days in df
  format = DateFormat("y-m-d")
  days = portfolio.Date[size(portfolio,1)] - portfolio.Date[1]

  # Calculate the CAGR
  cagr = ^((portfolio.total[size(portfolio,1)] / portfolio.total[1]), (252.0 / Dates.value(days))) - 1

  return cagr
  end

::

  # Call function and print output
  cagr = CAGR(portfolio)
  @printf("CAGR: %f\n", cagr)



.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.