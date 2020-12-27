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


Trend indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Momentum indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Volatility indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Volume indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**References**

* Murphy, J. J. (1991). Technical analysis of the futures markets: A comprehensive guide to trading methods and applications. New York: New York Institute of Finance.
* `CFI - Technical Analysis: A Beginner's Guide <https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/technical-analysis/>`_ # to delete

**Image sources**

.. [1] By Probe-meteo.com - Probe-meteo.com, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=26048221

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.