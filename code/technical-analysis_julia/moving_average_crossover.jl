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

@pyimport matplotlib.pyplot as plt

# load data
df = CSV.File("../../database/hkex_ticks_day/hkex_0001.csv") |> DataFrame

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

# create signals
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
plt.plot(signals.Date, signals.Close, color="red", linewidth=0.8, label="Closing price")
plt.plot(buy_signals.Date, buy_signals.Price, marker=10, markersize=7, color="m", linestyle="None", label="Buy signal")
plt.plot(sell_signals.Date, sell_signals.Price, marker=11, markersize=7, color="k", linestyle="None", label="Sell signal")

plt.title("MA crossover signals")
plt.show()

# save fig
fig.savefig("./figures/moving-average-crossover_signals", dpi=100)