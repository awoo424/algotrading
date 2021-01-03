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

There are 2 categories of indicators:

* **Leading** - They give trade signals when the trend is about to started, hence they use shorter
  periods in their calculations. Examples are MACD and RSI.
* **Lagging** - They follow the price action, and thus gives a signal after a trend or a reversal
  started. Examples are Moving Averages and Bollinger Bands.

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

  \text{%K} = \frac{\text{Current Close} - \text{Lowest Low})}{\text{Highest High} - \text{Lowest Low}} \times 100 \\
  \text{%D} = \text{3-day SMA of %K}

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



Money Flow Index (MFI)
""""""""""""""""""""""""""""""

William %R
""""""""""""""""""""""""""""""



Volatility indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| These indicators measure the rate of price movement, regardless of direction. 
  Generally, they are based on a change in the highest and lowest historical prices. 
  They provide useful information about the range of buying and selling that takes 
  place in a given market, and help traders determine points where the market may change direction.

Bollinger Bands
""""""""""""""""""""""""""""""

Average True Range
""""""""""""""""""""""""""""""

Standard Deviation
""""""""""""""""""""""""""""""


Volume indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chaikin Oscillator
""""""""""""""""""""""""""""""

On-Balance Volume (OBV)
""""""""""""""""""""""""""""""

Volume Rate of Change
""""""""""""""""""""""""""""""


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