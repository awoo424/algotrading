Introduction
=============

Welcome to the first tutorial for algorithmic trading!

In this tutorial, you will learn:

* The basics of algorithmic trading
* Definition of technical analysis
* Definition of fundamental analysis
* Difference between technical analysis and fundamental analysis

What is algo trading?
---------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Algorithmic trading** (a.k.a. algo trading) is the use of computer codes 
     and chart analysis to enter and exit trades automatically according to 
     set parameters such as price movements or volatility levels.

| In algo trading, one writes an algorithm and instruct a computer to buy or sell 
  stocks for you when the defined conditions are met. These programs can trade at 
  speed and frequency that is much higher than that of a human trader, and the process 
  can be semi-automated or completely automated. This is why sometimes we could use 
  the term **"automated trading"** interchangelably, but note that they are not 
  necesssarily referring to the same thing.

A typical algorithmic trading system does the following things (in order):

* Inspect data, charts, quotes or news and generate trade signals as per your strategy
* Fill in order details when a trade signal is found
* Monitor and evaluate trades to see if they reached your target or went in the opposite direction
* Close positions to either book profits or cut losses
* Rinse and repeat

Automated Trading
^^^^^^^^^^^^^^^^^^
| Automated Trading is the absolute automation of the trading process. Trading orders 
  are automatically created, submitted to the market and executed. Automated trading 
  facilities are usually utilized by hedge funds that exploit proprietary execution 
  algorithms and trade via Direct-Market Access (DMA) or sponsored access.

High-freqeuncy Trading
^^^^^^^^^^^^^^^^^^^^^^^
| High-frequency Trading (HFT) is a subset of automated trading. Technology has enabled 
  orders to be made within milliseconds. As execution speed is of a priority here, 
  HFT makes use of Direct-Market Access (DMA) in order to reduce the time transactions. 
  You can read more about HFT `here <https://www.forbes.com/sites/billconerly/2014/04/14/high-frequency-trading-explained-simply/#716eba0f3da8>`_.

.. tip:: 
    * **Algorithmic Trading**: execution process based on an algorithm
    * **Automated Trading**: as its name implies, automate the trading process
    * **High-frequency Trading**: ultra-fast automated trading


| There are two major schools of methods for analysing the market, 
  which are (1) technical analysis and (2) fundamental analysis. 
  We'll go through both of these in detail respectively in the coming tutorials.

What is technical analysis?
----------------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Technical analysis** is the study of market action, primarily through 
    the use of charts, for the purpose of forecasting future price trends. - *John J. Murphy*

| Here, the term *"market action"* (or price data, as some people call it) 
  refers to to any combination of the open, high, low, close, volume, or 
  open interest for a given security over a specific timeframe. The timeframe 
  can be based on intraday (1-minute, 5-minute, 10-minute, 15-minute, 
  30-minute or hourly), daily, weekly or monthly price data and last a few 
  hours or many years.

Rationale of technical analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Market Action Discounts Everything**

| This assumption states that any factor that could possibly affect the stock's 
  price - fundamental, political, psychological, or otherwise - is fully reflected 
  in the price of that stock. In other words, it is presumed that prices should 
  reflect shifts in demand and supply. For example, if prices are rising, no 
  matter the reasons behind, demand must exceed supply and thus the fundamentals 
  must be bullish. Conversely, if prices fall, the fundamentals must be bearish.

| Hence as a rule, technicians do not concern themselves with the reasons why 
  prices rise or fall. If everything that affects the market prices is ultimately 
  reflected in market price, then it makes sense that they study of that market price 
  is all that is necessary. That's why this assumption serves as a cornerstone for 
  technical analysis to work.

**2. Prices Move in Trends**

| Unless one accepts that markets do in fact trend, there's no point in reading any 
  further. Given the assumption that prices move in trends, we obtain the corollary 
  that a trend in motion is likely to continue than to reverse. Just like Newton's 
  first law of motion. The entire trend-following approach is predicated on riding 
  an existing trend, until a sign of reversing is observed.

**3. History repeats itself**

| Under this assumption, it is believed that the key to understanding the future 
  lies in a study of the past. Charts tend to form shapes that have occurred in 
  the past, and thus the analysis of historical patterns helps predict future 
  market movements.


Pros and cons of technical analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pros:

* Objectiveness
* Mathematical precision
* Emotional indifference
* Inexpensive

Cons:

* Self-fulfilling prophecy
* The future keeps running away
* Conflicting signals from different indicators
* Substantial movements might have taken place when a pattern is identified

What is fundamental analysis?
-----------------------------

| While technical analysis concentrates on the study of market action, 
  fundamental analysis focuses on the economic forces of supply 
  and demand that leads to price movements.

.. admonition:: Definition
   
   | The **fundamental analysis** approach examines all of the relevant factors affecting 
     the price of a stock in order to determine the intrinsic value of that 
     stock. - *John J. Murphy*

| The term *"intrinsic value"* here refers to what the stock is actually worth 
  based on the law of supply and demand. If the intrinsic value is below 
  the current market price, it means that the stock is overpriced and 
  thus it should be sold. Conversely, if the intrinsic value is above the 
  price, then the market is undervalued and that stock should be bought.

Rationale of fundamental analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| One of the primary assumptions of fundamental analysis is that the current price from the stock market 
  often does not fully reflect the value of a company. Thus, a fundamentalist would look at a company's 
  publicly available information and other economic data in order to gain an understanding of the company's 
  ability to create products and services, and to evaluate whether it is generating earnings in aproductive way.

| This approach stems from the assumption that the reported financial information is legitimate and correct. 
  A fundamentalist may also assume that a company's past performance and metrics may continue into the future. 


| Fundamental analysis consists of three main parts:

* **Economic analysis** - focuses on analysing various macroeconomic factors such as interest rates, inflation, and GDP levels
* **Industry analysis** - focuses on assessing specific prospects and potential opportunities within the identified industries and sectors
* **Company analysis** - focuses on analysing and selecting individual stocks within the most promising industries

| We could conduct fundamental analysis either in a **top-down approach** or **bottom-up approach**. By following the former, the investor
  will start with analysing the health of the overall economy, and then to determine the industry trends, and thus filter out promising companies
  within the industry. With regards to latter, it will be the reverse - beginning with individual stock analysis first, to find out stocks
  that could outperform the industry.


Pros and cons of fundamental analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pros:

* Seeks to understand the value of an asset
* Long-term view
* Comprehensive

Cons:

* Time-consuming
* Results not suitable for quick decisions
* Does not provide info about entry points*

| With regards to the last point, some investors would try to complement fundamental analysis by
  making use of technical analysis to decide entry points in the identified stocks.

Technical analysis vs Fundamental analysis
-------------------------------------------

| Both of these approaches intend to solve the same problem - to determine 
  the direction that prices are liekly to move. While technical analysis 
  focuses more on answering the question of "when to buy", fundamental analysis 
  helps us find an answer to the question of "what to buy".

.. important::
   
   | The fundamentalist studies the cause of market movement, while the 
     technician studies the effect. - *John J. Murphy*

| Theoretically, the technician would, according to the assumptions, ignore the 
  reasons that cause prices to change, and the fundamentalist would constantly be 
  digging into the causes of price movements. However, in reality there is a lot 
  of overlap between these two approaches, and they are not mutually exclusive. 
  **The problem of using a combination of both, is that the technical indicators 
  and fundamentals might come in conflict with each other**, and such descrepancies 
  especially occur at the most critical moments.

.. image:: ../images/Buy-low-and-sell-high.jpg
    :width: 275px
    :align: center
    :height: 162px
    :alt: "One does not simply buy low and sell high."

| Some people believe the fact that "market price tends to lead the known fundamentals" 
  accounts for this phenomenon. Put it in another way, it implies that the market price 
  acts as a leading indicator of the fundamentals. While the known fundamentals are already 
  reflected "in the market", they are now reacting to the unknown fundamentals, and thus 
  inducing the discrepancy.

| In learning about the premises of technical analysis, one can see why technicians 
  usually see their approach superior to fundamentalists'. Because, by definition, 
  if the fundamentals are reflected in the market price, then technical approach 
  includes the fundamental. Nevertheless, fundamental analysis does not include a 
  study of market action. Therefore, whilee it is feasible to trade solely relying 
  on technial approach, it is doubtful that anyone could trade off the fundamentals 
  alone without any consideration of the technical side of the market.


What is macroeconomic analysis in stock market?
-------------------------------------------
| The stock prices are often moved by some macroeconomic indicators, and hence it is 
  good to keep track of macroeconomic indicators. 

| Macroeconomic analysis is the study of relation between stock prices and macroeconomic
  indicators. 


What is sentiment analysis in stock market?
-------------------------------------------
Market sentiment refers to the overall attitude of investors toward a particular security. Investors profit by finding
stocks that are overvalued based on market sentiment



Conclusion
-----------

| Algorithmic Trading has become increasingly popular in the recent decade, and 
  it now accounts for the majority of trades in the market globally and has attributed 
  to the success of some of the world's best-performing hedgee funds. Indeed, 84% of 
  trades that happened in New York Stock Exchange (NYSE), and 60% in London Stock 
  Exchange (LSE) were all done using algorithmic trading. Therefore, whether one 
  is interested in making money with algo trading or not, studying algo trading 
  would definitely bring you insights on how technolgy has been applied in stock 
  markets and learn how algorithms have been shaping our modern day world.

**References**

* Murphy, J. J. (1991). Technical analysis of the futures markets: A comprehensive guide to trading methods and applications. New York: New York Institute of Finance.
* `CFI - Technical Analysis: A Beginner's Guide <https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/technical-analysis/>`_
* `IG - Technical Analysis definition <https://www.ig.com/en/glossary-trading-terms/technical-analysis-definition)>`_
* `FBS - Pros and Cons of Technical Analysis <https://fbs.com/analytics/tips/pros-and-cons-of-technical-analysis-and-indicators-21645>`_
* `CFI - What is Fundamental Analysis? <https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/fundamental-analysis/>`_

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.