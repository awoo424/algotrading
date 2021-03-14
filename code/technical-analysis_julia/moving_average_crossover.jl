import Pkg; 

Pkg.add("CSV") # install CSV
Pkg.add("DataFrames") # install Dataframes
Pkg.add("TimeSeries")
Pkg.add("Pandas")
Pkg.add("Plots") # plotting dataframe
Pkg.add("PyCall")
Pkg.add("RollingFunctions") # rolling functions

# import libraries
using CSV;
using Dates;
using DataFrames;
using Statistics;
using Plots;
using PyCall;
using RollingFunctions;
using Printf;

@pyimport matplotlib.pyplot as plt

# load data
df = CSV.File("../../database/microeconomic_data/hkex_ticks_day/hkex_0001.csv") |> DataFrame

ticker = "0001.HK"

# moving average crossover
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

# Create signals
signal = Float64[]
        
for i in 1:length(short_mavg)
    if short_mavg[i] > long_mavg[i]
        x = 1.0
    else
        x = 0.0
    end
    push!(signal, x)
end

insertcols!(signals, 1, :signal => signal)

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
#print(first(sell_signals,10)

# Plot signals and MAs

fig = plt.figure() # Initialise the plot figure
ax1 = fig.add_subplot(111, ylabel="Price in \$") # Add a subplot and label for y-axis

plt.plot(signals.Date, signals.short_mavg, color="blue", linewidth=1.0, label="Short MA")
plt.plot(signals.Date, signals.long_mavg, color="orange", linewidth=1.0, label="Long MA")
#plt.plot(signals.Date, signals.Close, color="red", linewidth=0.8, label="Closing price")
plt.plot(buy_signals.Date, buy_signals.Price, marker=10, markersize=7, color="m", linestyle="None", label="Buy signal")
plt.plot(sell_signals.Date, sell_signals.Price, marker=11, markersize=7, color="k", linestyle="None", label="Sell signal")

plt.title("MA crossover signals")
plt.show()

# save fig
fig.savefig("./figures/moving-average-crossover_signals", dpi=100)


# ============== Backtest ============== #

initial_capital = 100000.0

# Initialise the portfolio with value owned
portfolio = signals[:,[:Date, :Close, :positions]]
portfolio[:trade] = signals[:Close] .* (100 .* signals[:positions])

# Add `holdings` to portfolio
portfolio[:quantity] = cumsum(100 .* signals[:positions])
portfolio[:holdings] = portfolio[:Close] .* portfolio[:quantity]

# Add `cash` to portfolio
portfolio[:cash] = initial_capital .- cumsum(portfolio[:trade])

#  # Add `total` to portfolio
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

#print(first(portfolio, 100))
@printf("Final total value: %f\n", portfolio.total[size(portfolio,1)])

total_return = (portfolio.total[size(portfolio,1)] - portfolio.total[1]) / portfolio.total[1]
@printf("Total return: %f\n", total_return)

# ============== Evaluation metrics ============== #

function portfolio_return(portfolio)
    fig = plt.figure() # Initialise the plot figure
    ax1 = fig.add_subplot(111, ylabel="Total in \$") # Add a subplot and label for y-axis

    plt.plot(portfolio.Date, portfolio.returns, color="blue", linewidth=1.0, label="Returns")

    plt.title("MA crossover portfolio return")
    plt.show()

    # save fig
    fig.savefig("./figures/moving-average-crossover_returns", dpi=100)
end

function sharpe_ratio(portfolio)
    # Annualised Sharpe ratio
    sharpe_ratio = sqrt(252) * (mean(returns) / std(returns))

    return sharpe_ratio
end

function CAGR(portfolio)
    # Get the number of days in df
    format = DateFormat("y-m-d")
    days = portfolio.Date[size(portfolio,1)] - portfolio.Date[1]

    # Calculate the CAGR
    cagr = ^((portfolio.total[size(portfolio,1)] / portfolio.total[1]), (252.0 / Dates.value(days))) - 1
    
    return cagr
end


portfolio_return(portfolio)
sharpe = sharpe_ratio(portfolio)
cagr = CAGR(portfolio)

@printf("Sharpe ratio: %f\n", sharpe)
@printf("CAGR: %f\n", cagr)