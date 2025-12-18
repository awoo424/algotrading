Evaluation metrics
==============================

| This provides the explanation and equation of the evaluation metrics implemented
  in the backtester. The code could be found in :code:`code/evalaute.py` in the repository.


Portfolio return
-----------------------------

.. admonition:: Definition
   :class: myOwnStyle

   | **Portfolio return** is the percentage change in total value of the portfolio.

 
.. math::

    \text{Portfolio return} = \frac{\text{Current portfolio value} - \text{Previous portfolio value}}{\text{Previous portfolio value}} \times 100%


|

Sharpe ratio
-----------------------------

.. admonition:: Definition
   :class: myOwnStyle

   | **Sharpe ratio** computes the ratio of the return of an investment to its risk.


Mathematically, it is the average return earned in excess of the risk-free rate per unit of total volatility. 

.. math::

  \text{Sharpe Ratio} &= \frac{R_p - R_f}{\sigma_p} \\
  \\
  R_p &= \text{Portfolio return} \\
  R_f &= \text{Risk-free rate} (assumed = 0 in the function)\\
  \sigma_p &= \text{Portfolio risk, i.e. standard deviation}
 


|

Maximum drawdown (MDD)
-----------------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Maximum drawdown (MDD)** measures the maximum observed loss from a peak to 
     a trough of a portfolio. It is an indicator of downside risk over the given time period.

.. math::

    \text{MDD} &= \frac{\text{P} - \text{T}}{\text{P}} \\
    \\
    \text{P} &=  \text{Peak value before largest drop} \\
    \text{L} &=   \text{Lowest value before newest high established}


|

Compound Annual Growth Rate (CAGR)
-----------------------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Compoumd Annual Growth Rate (CAGR)** describes the rate at which an investment 
     would have grown if it had grown the same rate every year and the profits 
     were reinvested at the end of each year.

| It is used to smooth returns so that they may be more easily understood 
  when compared to alternative investments. Risk is not taken into account.


.. math::

  \text{CAGR} = \left(\frac{\text{Ending portfolio value}}{\text{Beginning portfolio value}}\right)^{252 \;\div\; \text{number of days}} - 1

| Note that "number of days" refers to the time span of the portfolio, and
  252 is the total number of trading days in one year.


|

Standard Deviation
-----------------------------

.. admonition:: Definition
   :class: myOwnStyle

  | **Standard Deviation** measures the dispersion of the historical portfolio values 
    relative to its mean. A higher standard deviation infers higher volatility.

.. math::

  \text{SD} &= \sqrt{\frac{\sum (r_i - r_{avg})^2 }{n-1}} \\
  \\
  r_i &= \text{Portfolio daily return} \\
  r_{avg} &= \text{Mean of portfolio daily returns}


| Note that sample SD is used, and thus the degree of freedom equals n-1 in the equation.


.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.