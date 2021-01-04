Techinical analysis
====================

In this tutorial, you will learn:

* The basics of technical analysis
* Technical analysis charts
* What are the common technical indicators
* How to implement technical indicators


Intro to technical analysis
-----------------------------

| As we have discussed in the first tutorial, technical analysis is a methodology for 
  predicting price movement through the study of market action in the past. Technical 
  analysis most commonly applies to price changes, but some technicians also track other 
  data such as trading volume and open interest figures. Within the industry, there exist 
  a tons of patterns and signals that have been developed by researchers in order to 
  conduct technical analysis trading. Some technical indicators are primarily focused on 
  identifying the current market trend, while some are aimed at spotting patterns in 
  historical patterns.

In general, technicians consider the following types of indicators:

* Price trends
* Chart analysis
* Volume indicators
* Momentum indicators
* Oscillators
* Moving averages


| In the upcoming tutorials for technical analysis, we will learn how to construct and 
  analyse charts with the help of programming; and to build and implement different 
  technical indicators widely used in the market. 

**Requirements:**

* `pandas <https://pypi.org/project/pandas/>`__
* `matplotlib <https://matplotlib.org>`__
* `numpy <https://numpy.org/>`__


Chart patterns
------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Bullish signal** means a signal to buy.
   | **Bearish signal** means a signal to sell.

Line chart
^^^^^^^^^^^^^^^^^^^^^^^

Candlesticks chart
^^^^^^^^^^^^^^^^^^^^^^^

| Candlestick charts originated in Japan over 100 years before the West developed the 
  bar and point-and-figure charts. In the 1700s, a Japanese man named Homma discovered 
  that, while there was a link between price and the supply and demand of rice, 
  the markets were strongly influenced by the emotions of traders. Candlesticks show 
  that emotion by visually representing the size of price moves with different colors. 
  Traders use the candlesticks to make trading decisions based on regularly 
  occurring patterns that help forecast the short-term direction of the price. 
  
.. role:: raw-html(raw)
    :format: html

.. figure:: ../images/Candlestick.png
    :width: 500px
    :align: center
    :height: 320px
    :alt: "Candlestick components."

    :raw-html:`<br />`
    Explanation of candlestick components. [1]_
    



Open-high-low-close (OHCL) chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Scaling 
^^^^^^^^^^

| There are two types of scales for plotting charts - **arithmetic** or **semi-logarithmic**. 
  As most of us who have studied science/mathematics should know, examples of logarithmic 
  scales include growth of microbes, mortality rate due to epidemics and so on. The 
  difference in scale can completely alter the shape of the chart even though it is 
  plotted using the same set of data. Semi-logarithmic charts are sometimes more 
  preferrable in order to overcome the weaknesses inherent in arithmetic charts.


Arithmetic scaling
""""""""""""""""""""
| In arithmetic or linear charts, both x and y axes scales are plotted at an equal distance.

.. admonition:: Key points
   :class: myOwnStyle
   
   * On a linear scale, as the distance in the axis increases the corresponding 
     value also increases linearly.
   * When the values of data fluctuate between extremely small values and very 
     large values – the linear scale will **miss out the smaller values** thus 
     conveying a wrong picture of the underlying phenomenon.   

Semi-logarithmic scaling
""""""""""""""""""""""""""""

| A semi-log plot is a graph where the data in one axis is on logarithmic scale 
  (either x axis or y axis), and data in the other axis is on normal scale (i.e. linear scale).

.. admonition:: Key points
   :class: myOwnStyle

   * On a logarithmic scale, as the distance in the axis increases the corresponding 
     value increases exponentially.
   * With logarithmic scale, **both smaller valued data and bigger valued data can be captured** 
     in the plot more accurately to provide a holistic view.

Therefore, semi-logarithmic charts can be of immense help especially when plotting **long-term charts**, 
or when the price points show significant volatility even in short-term charts. The underlying chart patterns 
will be revealed more clearly in semi-logarithmic scale charts.


Trend analysis
------------------




Technical indicators
----------------------

| The implementation of the below indicators could all be found in :code:`code/technical-analysis_python/` in
  the repository.

In general, there are 2 categories of indicators:

* **Leading** - They give trade signals when the trend is about to started, hence they use shorter
  periods in their calculations. Examples are MACD and RSI.
* **Lagging** - They follow the price action, and thus gives a signal after a trend or a reversal
  started. Examples are Moving Averages and Bollinger Bands.

| By calculating the technical indicators, we could create rules in order to generate entry points (i.e. buy and sell
  signals) in the market, and evaluate the performance of such a strategy using a **backtester**.

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Backtesting** is the process of applying a trading strategy 
     to historical data in order to evaluate the performance of the strategy.


| You could try running a strategy in the repository by:

:: 

  # in terminal
  cd code/technical-analysis_python
  python main_macd_crossover.py # run macd in the backtester

| The following provides the explanation and equations for all the example strategies featured
  in the repository.

Trend indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Trend indicators measure the direction and strength of a trend, using 
  some form of price averaging to establish a baseline.


.. admonition:: Definition
   :class: myOwnStyle

   | **Exponential Moving Average (EMA)** (a.k.a. exponentially weighted moving average) 
     is a type of moving average (MA) that places a greater weight and significance on the most recent data points. 


Moving Average Convergence Divergence (MACD)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
| The Moving Average Convergence Divergence (MACD) indicator is used to reveal changes in strength, direction, momentum and 
  duration of a trend in a stock’s price.

.. math::

    \text{MACD} = \text{12-Period EMA} − \text{26-Period EMA}

One of the simplest strategy established with MACD, is to identify MACD **crossovers**. The rules are as follows.

.. tip:: 
    * **Buy signal**: MACD rises above the signal line
    * **Sell signal**: MACD falls below the signal line

It is easy to calculate the EMA with pandas:

:: 

    # Get adjusted close column
    close = self.df['Close']

    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2

| :code:`span` specifies the time span, and :code:`adjust=False` means the 
  exponentially weighted function is calculated recursively (as we do not need
  a decaying adjustment factor for beginning periods).

.. math::

    \text{Signal Line} = \text{9-day EMA of MACD Line}

To plot the signal line:

::

    df['Signal line'] = self.df['MACD'].ewm(span=9, adjust=False).mean()


Moving Averages (MA)
""""""""""""""""""""
| Moving Averages (MA) are used to identify current trends and trend reversals, as well as 
  to set up support and resistance levels.

We could estalish a simple trading strategy making use of two moving averages:

.. tip:: 
    * **Buy signal**: shorter-term MA crosses above the longer-term MA **(golden cross)**
    * **Sell signal**: shorter-term MA crosses below the longer-term MA **(dead/death cross)**

Here is an example of how to plotting the two MAs: 
::

    # Create short simple moving average over the short window
    signals['short_mavg'] = self.df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

    # Create long simple moving average over the long window
    signals['long_mavg'] = self.df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

| We could define the :code:`short_window` and :code:`long_window` on our own, for example as setting
  :code:`short_window = 40` and :code:`long_window = 40`.

And then we could generate signals based on the two line plots:

::

    # Generate signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                                > signals['long_mavg'][self.short_window:], 1.0, 0.0)
    
    signals['positions'] = signals['signal'].diff()   

Parabolic Stop and Reverse (Parabolic SAR)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

| The Parabolic Stop and Reverse (Parabolic SAR) indicator used to find potential reversals in the market price direction.

| We need to calculate the **rising SAR** and **falling SAR** respectively:

**(i) Rising SAR (Uptrend)**

.. math::

    \text{Current SAR} = \text{Prior SAR} + \text{Prior AF} \times (\text{Prior EP} - \text{Prior SAR})

| where:

* **Prior SAR**: The SAR value for previous period. 
* **Extreme Point (EP)**: The highest high of the current uptrend. 
* **Acceleration Factor (AF)**: Starting at 0.02, increases by 0.02 each time the extreme point makes a new high. 
  AF can only reach a maximum of 0.2, no matter how long the uptrend extends.

| Note that for rising SAR, the SAR can never be above the prior two periods' lows. 
  Should SAR be above one of those lows, use the lowest of the two for SAR.  

**(ii) Falling SAR (Downtrend)**

.. math::
    
    \text{Current SAR} = \text{Prior SAR} + \text{Prior AF} \times (\text{Prior EP} - \text{Prior SAR})

| where:

* **Prior SAR:** The SAR value for previous period. 
* **Extreme Point (EP):** The lowest low of the current downtrend. 
* **Acceleration Factor (AF):** Starting at 0.02, increases by 0.02 each time the extreme point 
  makes a new low. AF can only reach a maximum of 0.2, no matter how long the downtrend extends.

| Note that for falling SAR, the SAR can never be below the prior two periods' highs. 
  Should SAR be below one of those highs, use the highest of the two for SAR. 

We generate signals based on the rising and falling SARs.

.. tip:: 
    * **Buy signal**: if falling SAR goes below the price
    * **Sell signal**: if rising SAR goes above the price

| In the code, we first need to extract the high / low / closing prices column from the dataframe, 
  and initialise the arrays for storing the rising SAR and falling SAR:

:: 

    array_high = list(df['High'])
    array_low = list(df['Low'])
    array_close = list(df['Close'])

    psar = df['Close'].copy()
    psarbull = [None] * len(df)
    psarbear = [None] * len(df)
    
    bull = True # flag to indicate saving value for rising SAR
    af = initial_af # initialise acceleration factor
    max_af = 0.2
    ep = array_low[0] # extreme price
    hp = array_high[0] # extreme high
    lp = array_low[0] # extreme low

Then, traversing each row in the dataframe, we could calculate rising SAR and falling SAR at the same time:

::

    for i in range(2, len(self.df)):
      if bull:
          # Rising SAR
          psar[i] = psar[i-1] + af * (hp - psar[i-1])
      else:
          # Falling SAR
          psar[i] = psar[i-1] + af * (lp - psar[i-1])

        reverse = False

        # Check reversion point
        if bull:
            if array_low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = array_low[i]
                af = initial_af
        else:
            if array_high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = array_high[i]
                af = initial_af

        if not reverse:
            if bull:
                # Extreme high makes a new high
                if array_high[i] > hp:
                    hp = array_high[i]
                    af = min(af + initial_af, max_af)

                # Check if SAR goes abov prior two periods' lows. 
                # If so, use the lowest of the two for SAR.
                if array_low[i-1] < psar[i]:
                    psar[i] = array_low[i-1]
                if array_low[i-2] < psar[i]:
                    psar[i] = array_low[i-2]

            else:
                # Extreme low makes a new low
                if array_low[i] < lp:
                    lp = array_low[i]
                    af = min(af + initial_af, max_af)

                # Check if SAR goes below prior two periods' highs. 
                # If so, use the highest of the two for SAR.
                if array_high[i-1] > psar[i]:
                    psar[i] = array_high[i-1]
                if array_high[i-2] > psar[i]:
                    psar[i] = array_high[i-2]

        # Save rising SAR
        if bull:
            psarbull[i] = psar[i]
        # Save falling SAR
        else:
            psarbear[i] = psar[i]



Momentum indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Momentum indicators help identify the speed of price movement by comparing prices
  over time. Typically when there is a divergence between price and a momentum indicator,
  it can signal a change in future prices.

Commodity Channel Index (CCI)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

| The Commodity Channel Index (CCI) helps identify price reversals, price extremes, and trend strength.

| Developed by Donald Lambert, CCI is a momentum-based oscillator used to 
  help determine when an investment vehicle is reaching a condition of 
  being **overbought or oversold**. It is also used to assess price 
  trend direction and strength. This information allows traders 
  to determine if they want to enter or exit a trade, refrain 
  from taking a trade, or add to an existing position.

The formula for calculating CCI is given as follow.

.. math::

  \text{CCI} = \frac{(\text{Typical Price} - \text{x-period SMA of TP})}{(\text{Constant} \times \text{Mean Deviation})}

| where:

* Typical Price (TP) = (High + Low + Close) / 3
* Constant = 0.015
* x = Window size (default set as 20)
* SMA: Simple Moving Average 


| We could first compute the the subcomponents of CCI:

::

  signals['Typical price'] = (df['High'] + df['Low'] + df['Close']) / 3
  
  signals['SMA'] = signals['Typical price'].rolling(
                   window=self.window_size, min_periods=1, center=False).mean()

  signals['mean_deviation'] = signals['Typical price'].rolling(
                              window=20, min_periods=1, center=False).std()

| Then calculate CCI using the formula:

:: 

  signals['CCI'] = (signals['Typical price'] - signals['SMA']) /
                   (self.constant * signals['mean_deviation'])

A simple strategy formulated by using CCI is (the thresholds only serve as examples:

.. tip:: 
    * **Buy signal**: when CCI surges above +100
    * **Sell signal**: when CCI plunges below -100

| To implement this rule in code:

::

  # Generate buy signal
  signals.loc[signals['CCI'] > 100, 'signal'] = 1.0

  # Generate sell signal
  signals.loc[signals['CCI'] < -100, 'signal'] = -1.0


Relative Strength Index (RSI)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

| The Relative Strength Index (RSI) measures recent trading strength, velocity of change in the trend, 
  and magnitude of the move.

.. math::

    \text{RSI} = 100 - \frac{100}{(1 + \text{RS})} \\ \\
    \text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}} \\

where **Average Gain** and **Average Loss** are calculated as follows:

.. math::

    \text{First Average Gain} = \frac{\text{Sum of gains over the past 14 periods}}{14} \\ \\
    \text{First Average Loss} = \frac{\text{Sum of losses over the past 14 periods}}{14} \\ \\

    \text{Average Gain} = \frac{\text{Previous average gain} \times 13 + \text{Current gain}}{14} \\ \\
    \text{Average Loss} = \frac{\text{Previous average loss} \times 13 + \text{Current loss}}{14} \\ \\


| Note that the first calculations are just simple 14-period averages. Subsequent averages
  take the prior value plus the current value to compute the average. This is a smoothing technique 
  similar to that used in calculating an exponential moving average. Thus, the RSI values become 
  more accurate as the calculation period extends.

In the dataset, we need to extract gains and losses from the price column respectively:

::

    # Get adjusted close column
    close = df['Close']

    # Get the difference in price from previous step
    delta = close.diff()
    # Get rid of the first row
    delta = delta[1:] 

    # Make the positive gains (up) and negative gains (down) series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0


To calculate RS, as well as RSI:

::

    # Calculate SMA using 'rolling' function
    roll_up = up.rolling(window_size).mean()
    roll_down = down.abs().rolling(window_size).mean()

    # Calculate RSI based on SMA
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))

| The output of the RSI is a number on a scale **from 0 to 100** and it is 
  typically calculated on a 14-day basis. To generate the trading signals, 
  it is common to **specify the low and high levels of the RSI** (e.g. at 30 and 70 respectively).
  The interpretation of the thresholds is that the lower one 
  indicates that the asset is oversold, and the upper one that the asset is 
  overbought.

.. tip:: 
    * **Oversold**: when RSI crosses the lower threshold (e.g. 30)
    * **Overbought**: when RSI crosses the upper threshold (e.g. 70)


Rate of Change (ROC)
""""""""""""""""""""""""""""

| The Rate of Change (ROC) measures the strength of price momentum. 

| **Positive values** of the ROC indicates upward buying pressure or momentum, while 
  **negative values** below zero indicate selling pressure or downward momentum. 
  Increasing values in either direction, positive or negative, indicate increasing momentum, 
  and decreasing values indicate waning momentum.

.. math::

  \text{ROC} = 
  \frac{(\text{Closing price} - \text{Closing price n periods ago})}{(\text{Closing price n periods ago})} \times 100

As you could see from above, it's just the simple percentage change formula.

We could identify overbought and oversold conditions using ROC:

.. tip:: 
    * **Oversold**: when ROC crosses the lower threshold (e.g. -30)
    * **Overbought**: when ROC crosses the upper threshold (e.g. +30)

And here is one of the possible ways to calculate ROC:

::

    n = 12 # set time period

    diff = df['Close'].diff(n - 1)

    # Calculate closing price n periods ago
    closing = self.df['Close'].shift(n - 1)

    df['ROC'] = (diff / closing) * 100

Stochastic Oscillator (STC)
""""""""""""""""""""""""""""""

| Stochastic Oscillators (STC) are used to predict price turning points by comparing the closing price to its price range.

.. math::

  \text{%K} &= \frac{\text{Current Close} - \text{Lowest Low})}{\text{Highest High} - \text{Lowest Low}} \times 100 \\ 
  \\
  \text{%D} &= \text{3-day SMA of %K}

| where:

* Lowest Low = lowest low for the look-back period
* Highest High = highest high for the look-back period

Note that in the formula %K is multiplied by 100 so as to move the decimal point by two places.

| We could traverse the dataframe and store all highests highs, lowest lows in two separate arrays:

::

    array_highest = [0] * length # store highest highs
    for i in range(k - 1, length):
        highest = array_high[i]
        for j in range(i - 13, i + 1): # k-day lookback period
            if array_high[j] > highest:
                highest = array_high[j]
        array_highest[i] = highest
          
    array_lowest = [0] * length # store lowest lows
    for i in range(k - 1, length):
        lowest = array_low[i]
        for j in range(i - 13, i + 1): # k-day lookback period
            if array_low[j] < lowest:
                lowest = array_low[j]
        array_lowest[i] = lowest

| Then, we can calculate %K and %D:

::

    # find %K line values
    kvalues = [0] * length

    for i in range(self.k - 1, length):
        k = ((array_close[i] - array_lowest[i]) * 100) / (array_highest[i] - array_lowest[i])
        kvalues[i] = k

    df['%K'] = kvalues

    # find %D line values
    df['%D'] = df['%K'].rolling(window=3, min_periods=1, center=False).mean()

| A strategy established with %K and %D is as follows:

.. tip:: 
    * **Buy signal**: when %K line crosses above the %D line
    * **Sell signal**: when %K line crosses below the %D line


True Strength Index (TSI)
""""""""""""""""""""""""""""

| The True Strength Index (TSI) is a momentum oscillator based on a double smoothing of price changes. 
  By smoothing price changes, it captures the ebbs and flows of price action with a steadier line that 
  tries to filter out noises.

.. math::

  \text{TSI} = \frac{\text{Double Smoothed PC}}{\text{Double Smoothed Absolute PC}} \times 100

| where:

**(i) Double Smoothed Price Change (PC)**

* PC = Current Price - Prior Price
* First Smoothing = 25-period EMA of PC
* Second Smoothing = 13-period EMA of 25-period EMA of PC

**(ii) Double Smoothed Absolute Price Change (PC)**

* Absolute Price Change | PC | = Absolute Value of Current Price minus Prior Price
* First Smoothing = 25-period EMA of | PC |
* Second Smoothing = 13-period EMA of 25-period EMA of | PC |

Based on the above formulae, the code is shown as follow:

:: 

  df['Double Smoothed PC'] = pc.ewm(span=25, adjust=False).mean().ewm(
                                  span=13, adjust=False).mean()

  df['Double Smoothed Abs PC'] = abs(pc).ewm(span=25, adjust=False).mean().ewm(
                                      span=13, adjust=False).mean()

  df['TSI'] =  df['Double Smoothed PC'] / df['Double Smoothed Abs PC'] * 100


In order to interpret the TSI, we could define a signal line:

.. math::
  
    \text{Signal line} = \text{10-period EMA of TSI}

And we could observe signal line crossovers:

.. tip:: 
    * **Buy signal**: when TSI crosses above the signal line from below
    * **Sell signal**: when TSI crosses below the signal line from above



Money Flow Index (MFI)
""""""""""""""""""""""""""""""

| The Money Flow Index (MFI) is an oscillator that generates overbought or 
  oversold signals using both prices and volume data.


.. math::

  \text{Money Flow Index} &= 100 - \frac{100}{(1 + \text{Money Flow Ratio})} \\
  \\
  \text{Raw Money Flow} &= \text{Typical Price} \times \text{Volume} \\
  \\
  \text{Typical Price} &= \frac{(\text{High} + \text{Low} + \text{Close})}{3} \\
  \\
  \text{Money Flow Ratio} &= \frac{\text{14-period Positive Money Flow}}{\text{14-period Negative Money Flow}} \\

It is pretty straightforward to calculate typical price:

::

  # Typical price
  tp = (df['High'] + df['Low'] + df['Close']) / 3.0


| With regards to the positive and negative money flows, we will first want to compute the raw money flow,
  then label which of them belong to positive / negative respectively:

::

  # positive = 1, negative = -1
  self.df['Sign'] = np.where(tp > tp.shift(1), 1, np.where(tp < tp.shift(1), -1, 0))

  # Raw money flow
  df['Money flow'] = tp * df['Volume'] * df['Sign']

  # Positive money flow with n periods
  n_positive_mf = df['Money flow'].rolling(n).apply
                  (lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True)
  
  # Negative money flow with n periods
  n_negative_mf = abs(df['Money flow'].rolling(self.n).apply
                  (lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True))

With the money flows, it would be easy to compute the MFI:

::

  mf_ratio = n_positive_mf / n_negative_mf
  df['MFI'] = (100 - (100 / (1 + mf_ratio)))


By way of example, we could use MFI to identify overbought and oversold conditions:

.. tip:: 
    * **Oversold**: when MFI crosses the upper threshold
    * **Overbought**: when MFI crosses the lower threshold


William %R
""""""""""""""""""""""""""""""

| William %R reflects the level of the close relative to the highest high for the look-back period.

.. math::

  \text{%R} = \frac{\text{Highest High} - \text{Close}}{\text{Highest High} - \text{Lowest Low}} \times -100

| where:

* Lowest Low = lowest low for the look-back period
* Highest High = highest high for the look-back period

| Note that in the formula, %R is multiplied by -100 to correct the inversion and move the decimal. 
  The default setting for the lookback period is 14, which can be days, weeks, months or an intraday timeframe.

The code for implementing %R is shown as follows:

:: 

  lbp = 14 # set lookback period
  
  hh = df['High'].rolling(lbp).max()  # highest high over lookback period
  ll = df['Low'].rolling(lbp).min()  # lowest low over lookback period
  df['%R'] = -100 * (hh - df['Close']) / (hh - ll)

Similarly, we could use %R to identify overbought and oversold conditions:

.. tip:: 
    * **Oversold**: when %R goes below -80
    * **Overbought**: when %R goes above -20


Volatility indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| These indicators measure the rate of price movement, regardless of direction. 
  Generally, they are based on a change in the highest and lowest historical prices. 
  They provide useful information about the range of buying and selling that takes 
  place in a given market, and help traders determine points where the market may change direction.

Bollinger Bands
""""""""""""""""""""""""""""""

| The Bollinger Bands indicator is used to measure the “highness” or “lowness” of the price, 
  relative to previous trades.

| The Bollinger Bands consist of a middle band with two outer bands:

.. math::

    \text{Middle Band} &= \text{20-day simple moving average (SMA)} \\
    \text{Upper Band} &= \text{20-day SMA} + (\text{20-day standard deviation of price} \times 2) \\
    \text{Lower Band} &= \text{20-day SMA} - (\text{20-day standard deviation of price} \times 2)


| We could first compute the middle band and the 20-day standard deviation:

::

  window = 20

  # Compute middle band
  df['Middle band'] = self.df['Close'].rolling(window).mean()

  # Compute 20-day s.d.
  mstd = df['Close'].rolling(window).std(ddof=0)

| Then we could get the outer bands:

::

  # Computer upper and lower bands
  df['Upper band'] = df['Middle band']  + mstd * 2
  df['Lower band'] = df['Middle band']  - mstd * 2


| The signals could be derived from observing the below conditions:

.. tip:: 
    * **Buy signal**: when price goes below lower band
    * **Sell signal**: when price goes above upper band


Average True Range
""""""""""""""""""""""""""""""

| Average True Range (ATR) is an indicator that tries to measure the degree of price volatility.

.. math::

  \text{Current ATR} = \frac{(Prior ATR \times 13) + Current TR}{n}

| where:

* 1st True Range (TR) value = High - Low
* 1st n-day ATR = average of the daily TR values for the last n days

| The True Range could be computed by:

::

  array_high = list(df['High'])
  array_low = list(df['Low'])

  tr = [None] * len(df) # initialisation

  for i in range(len(df)):
      tr[i] = array_high[i] - array_low[i]

| We would first calculate the first n-day ATR:

::

    atr = [None] * len(self.df) # initialisation
    window = 14

    atr[15] = sum(tr[0:15]) / window
    
| Then for the following ATRs:

::

  for i in range(16,len(self.df)):
      atr[i] = (atr[i-1] * (window-1) + tr[i]) / window

| We could determine whether the stock is **highly volatile** by checking the following conditions:

.. math::
    \text{50-day EMA} &> \text{200-day EMA} \\
    \\
    &\textbf{AND} \\
    \\
    \frac{\text{250-day ATR}}{\text{20-day SMA}} &\times 100 < 4

.. tip:: 
  We could use ATR to filter out stocks that are **highly volatile**.


Standard Deviation
""""""""""""""""""""""""""""""

| Standard Deviation measures expected risk and determines the significance of certain price movements.

As an example, we could set :code:`window=21`:

::

  window = 21
  df['SD'] = df['Close'].rolling(window).std(ddof=0)

.. tip:: 
  We could use Standard Deviation to measure the **expected risk** of stocks.

Volume indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Volume indicators measure the strength of a trend or confirm a trading direction 
  based on some form of averaging or smoothing of raw volume. The strongest 
  trends often occur while volume increases; in other words, some would assume that
  it is the increase in trading volume that can lead to large movements in price.



Chaikin Oscillator
""""""""""""""""""""""""""""""

| The Chaikin Oscillator indicator monitors the flow of money in and out of the market.
  By comparing money flow to price action, it helps identify tops and bottoms in short and intermediate cycles.

.. math::

  \text{Chaikin Oscillator} &= \text{3-day EMA of ADL} - \text{10-day EMA of ADL} \\
  \\
  \text{Accumulation Distribution Line (ADL)} &= \text{Previous ADL} \\
  &+ \text{Current Period's Money Flow Volume} \\
  \\
  \text{Money Flow Volume} &= \text{Money Flow Multiplier} \\
  &\times \text{Volume for the Period} \\
  \\
  \text{Money Flow Multiplier} &= \frac{(\text{Close} - \text{Low}) - (\text{High} - \text{Close})}{(\text{High} - \text{Low})} 


| We would first calculate the Money Flow Multiplier:

::

  df['MFM'] = ((df['Close'] - df['Low']) - df['High'] - df['Close']) 
              / (df['High'] - df['Low'])

| Then use it to calculate Money Flow Volume:

::

  df['MFV'] = df['MFM'] * df['Volume']

| Following, we could compute ADL and the Chaikin Oscillator:

::

  df['ADL'] = df['Close'].shift(1) + df['MFV']

  short_w = 3
  long_w = 10
  ema_long = df['ADL'].ewm(ignore_na=False, min_periods=0, com=short_w, adjust=True).mean()
  ema_short = df['ADL'].ewm(ignore_na=False, min_periods=0, com=long_w, adjust=True).mean()
  
  df['Chaikin'] = ema_short - ema_long

| We could establish the following simple strategy, as an example:

.. tip:: 
    * **Buy signal**: when the oscillator is positive
    * **Sell signal**: when the oscillator is negative


On-Balance Volume (OBV)
""""""""""""""""""""""""""""""

| The On Balance Volume indicator attempts to measure the level of accumulation or 
  distribution by comparing volume to price movements.


The formula for OBC changes according to the following 3 cases:

**1) If closing price > prior close price:**

.. math::

    \text{Current OBV} = \text{Previous OBV} + \text{Current Volume}

**2) If closing price < prior close price:**

.. math::

    \text{Current OBV} = \text{Previous OBV} - \text{Current Volume}

**3) If closing price = prior close price then:**

.. math::

    \text{Current OBV} = \text{Previous OBV (no change)}

We could traverse the dataframe, and use if-else statements to capture the 3 conditions: 

::

    obv = [0] * len(self.df) # for storing the on-balance volume

    array_close = list(df['Close'])
    array_volume = list(df['Volume'])

    for i in range(1, len(self.df)):
        if (array_close[i] > array_close[i-1]):
            obv[i] = obv[i-1] + array_volume[i]
        elif (array_close[i] < array_close[i-1]):
            obv[i] = obv[i-1] - array_volume[i]
        else:
            obv[i] = obv[i-1]

| The absolute value of OBV is not important. We should instead focus on the characteristics of the OBV line
  and its the trend.
  
.. tip::
  * A rising OBV reflects positive volume pressure that can lead to **higher prices**
  * A falling OBV reflects negative volume pressure that can foreshadow **lower prices** 


Volume Rate of Change 
"""""""""""""""""""""""""""""""""""

| The Volume Rate of Change (Volume ROC) highlights increases in volume, which normally occurs 
  at most significant market tops, bottoms and breakouts.

.. math::

  \text{Volume Rate of Change} = \frac{\text{Volume (today)} - \text{Volume (n days ago)}}{\text{Volume (n days ago)}}


The way of calculating Volume ROC is similar to ROC:

::

  n = 25 # example time period
  df['Volume ROC'] = ((df['Close'] - df['Close'].shift(n)) / 
                      df['Close'].shift(n))

Here is a simple example strategy based on Volume ROC:

.. tip:: 
    * **Buy signal**: if Volume ROC goes below zero
    * **Sell signal**: if Volume ROC is negative


**References**

* `Investopedia <https://www.investopedia.com>`_
* `StockCharts <https://school.stockcharts.com>`_
* `Parabolic SAR <https://virtualizedfrog.wordpress.com/2014/12/09/parabolic-sar-implementation-in-python/>`_

**Image sources**

.. [1] By Probe-meteo.com - Probe-meteo.com, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=26048221

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.