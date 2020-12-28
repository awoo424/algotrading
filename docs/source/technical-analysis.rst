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
| They are used to reveal changes in strength, direction, momentum and 
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


Moving averages
""""""""""""""""""""
| They are used to identify current trends and trend reversals, as well as 
  to set up support and resistance levels.


Parabolic Stop and Reverse (Parabolic SAR)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

| They are used to find potential reversals in the market price direction.



Momentum indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Commodity Channel Index (CCI)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

| They help identify price reversals, price extremes, and trend strength.

| Developed by Donald Lambert, CCI is a momentum-based oscillator used to 
  help determine when an investment vehicle is reaching a condition of 
  being **overbought or oversold**. It is also used to assess price 
  trend direction and strength. This information allows traders 
  to determine if they want to enter or exit a trade, refrain 
  from taking a trade, or add to an existing position. 

Relative Strength Index (RSI)
""""""""""""""""""""""""""""""""""""""""""""""""""""""

| They measure recent trading strength, velocity of change in the trend, 
  and magnitude of the move.

.. math::

    \text{RSI} = 100 - \frac{100}{(1 + \text{RS})} \\ \\
    \text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}} \\

where **Average Gain** and **Average Loss** are calculated as follows:

.. math::

    \text{First Average Gain} = \frac{\text{Sum of gains over the past 14 periods}}{14} \\ \\
    \text{First Average Loss} = \frac{\text{Sum of losses over the past 14 periods}}{14} \\ \\

    \text{Average Gain} = \frac{\text{Previous average gain} \times 13 + \text{Current gain}}{14} \\ \\
    \text{Average Loss} = \frac{[\text{Previous average loss} \times 13 + \text{Current loss}}{14} \\ \\


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
    * **Oversold**: when RSI crosses the lower threshold (e.g. 30).
    * **Overbought**: when RSI crosses the upper threshold (e.g. 70).


Rate of Change (ROC)
""""""""""""""""""""""""""""

Stochastic Oscillator (STC)
""""""""""""""""""""""""""""""

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

**Image sources**

.. [1] By Probe-meteo.com - Probe-meteo.com, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=26048221

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.