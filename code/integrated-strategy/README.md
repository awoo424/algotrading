## Integrated Strategy
The following strategies have been implemented in Python:

#### Baseline model
* `baseline.py` (for one ticker)
* `baseline_wrapper.py` (for a set of tickers)
  
#### Single-feature LSTM model 
* `LSTM-train_price-only.py` (for one ticker)
* `LSTM-train_price-only_wrapper.py` (for a set of tickers)

#### Multi-feature LSTM model
* `LSTM-train_wrapper.py` (for a set of tickers)

#### Multi-feature LSTM model with paper trading in IB
* `LSTM-train_daily.py` (for training the model)
* `daily_trading_strategy.py` (for generating the daily trading signal)
* `daily_trading_order.py` (for making the order via IB)