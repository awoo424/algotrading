Data science basics
====================

In this tutorial, you will learn to:

* Conduct Exploratory Data Analysis (EDA)
* Carry out resampling
* Visualise time series data
* Calculate and plot distribution of percentage change
* Use moving windows


**Requirements:**

* `pandas <https://pypi.org/project/pandas/>`__
* `matplotlib <https://matplotlib.org>`__
* `numpy <https://numpy.org/>`__


Exploratory Data Analysis
--------------------------

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Exploratory Data Analysis** (a.k.a. EDA) is the process of performing initial investigations 
     on the data so as to discover patterns, spot anomalies and to check assumptions with the help of 
     summary statistics and graphical representations.

For example, in the process of EDA, aim to find the answer to these questions:

* What kind of data does the dataframe store?
* What is the range of each column?
* What is the data type of each column?
* Are there null values in the data?

::

    # import AAPL csv file
    aapl = pd.read_csv('../../database/nasdaq_ticks_day/nasdaq_AAPL.csv', header=0, index_col='Date', parse_dates=True)

    # inspect first 5 rows (default)
    aapl.head()

    # inspect first 3 rows
    aapl.head(3)


::

    # check name of columns
    aapl.columns

    # output
    # aapl.columns

::

    # generate descriptive statistics, e.g. central tendency and dispersion of the dataset 
    # (excl. NaN values)
    aapl.describe()

    # prints a summary of the dataframe e.g. dtype, non-null values
    aapl.info()

::

    # print rows between two specific dates
    print(aapl.loc[pd.Timestamp('2020-07-01'):pd.Timestamp('2020-07-17')])

    # select only data between 2006 and 2019
    aapl = aapl.loc[pd.Timestamp('2006-01-01'):pd.Timestamp('2019-12-31')]
    aapl.head()


Resampling
------------------

It is easy to mix up **sampling** and **resampling**, which are indeed referring to two different concepts. 
We will first take a look at the definition of the former:

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Sampling** is the process of gathering observations with the intent to estimate a 
     population variable.

Assume that each row of data represents an observation about something in the world. When working with data, 
we usually do not have access to all possible observations since they might be hard to gather, or it might be
to costly to process them altogether. Thus, we use sampling as a solution - to select some part of the population 
to observe, so that we can infer something about the whole population.

For example, we can conduct **Simple Random Sampling**, which means that each row (or observation) is drawn 
with a uniform probability from the dataset.
::
    
    # Take 10 rows from the dataframe randomly
    sample = aapl.sample(10)
    print(sample)

Now that we understand what sampling is, let's go back to resampling.

.. admonition:: Definition
   :class: myOwnStyle
   
   | **Resampling** is a method that uses a data sample to improve the accuracy and 
     quantify the uncertainty of a population parameter.

As a data sample might not accurately represent the popultion, it introduces the problems of 
**Selection Bias** and **Sampling Error**.

* **Selection Bias** occurs when the method of drawing observations skews the sample in some way.
* **Sampling Error** occurs when randomly drawing observations skews the sample in some way.

To address this problem, we want to know how accruately the data sample is estimating the 
population parameter (e.g. the mean, or the standard deviation).

If we only sample that data once, we will only have one single estimate of the population parameter, 
which makes it impossible to quantify the uncertainty of the estimate. (Assuming we do not have the population data) 
Therefore, we could try estimate the population parameter *multiple times* from our data sample - we call this action, 
**resampling**.

With regards to the *resample* function in pandas, it is used for changing the time interval of a dataset. Thus, we
need a datetime type index or column in order to use the function.

::

    # Resample to monthly level
    monthly_aapl = aapl.resample('M').mean()
    print(monthly_aapl)

As shown in the code above, there are two steps in calling the function:

1. Pass the **'Rule'** argument to the function, which determines by what interval the data will be resampled by.
   In the example above, 'M' means by month end frequency.
2. Decide how to **reduce the old datapoints** or fill in the new ones, by calling groupby aggregate functions including mean(), min(), max(), sum().

In the above example, as we are resampling that data to a wider time frame (from days to months), we are actually
**"downsampling"** the data.

On the other hand, if we resample the data to a shorter time frame (from days to minutes), it will be called **"upsampling"**:

::

    # Resample to minutely level
    minutely_aapl = aapl.resample('T').ffill()
    print(minutely_aapl)

As we end up having additional empty rows in the resulting table, we need to decide how to fill in them with numeric values:

* :code:`ffill()` ‘Forward filling’ or :code:`pad()`‘padding’ — Use the last known value.
* :code:`bfill()` or :code:`backfill()` ‘Backfilling’ — Use the next known value.


Calculate percentage change
---------------------------------

We can just directly use the :code:`pct_change()` function to do this.

::

    daily_close = aapl[['Close']]

    # Calculate daily returns
    daily_pct_change = daily_close.pct_change()

    # Replace NA values with 0
    daily_pct_change.fillna(0, inplace=True)

    # Inspect daily returns
    print(daily_pct_change.head())

::

    # Calculate daily log returns
    daily_log_returns = np.log(daily_close.pct_change()+1)

    # Print daily log returns
    print(daily_log_returns.head())

We can also combine with the operation of resampling to get the percentage change of different time intervals.

::

    # Resample to business months, take last observation as value 
    monthly = aapl.resample('BM').apply(lambda x: x[-1])

    # Calculate monthly percentage change
    monthly.pct_change().tail()

This example takes the mean instead of the last observation in each bin as the value.

::

    # Resample to quarters, take the mean as value per quarter
    quarter = aapl.resample("4M").mean()

    # Calculate quarterly percentage change
    quarter.pct_change().tail()

It is also good to learn how to manually do the calculation, without using the :code:`pct_change()` function.

::

    # Daily returns
    daily_pct_change = daily_close / daily_close.shift(1) - 1

    # Print `daily_pct_change`
    daily_pct_change.tail()


Visualise time series data
---------------------------------

We will mainly use plotting functions provided by matplotlib. **Line plot** is the most common
type of plot that we will use for analysis of stock data.

::

    # Plot the closing prices for `aapl`
    aapl['Close'].plot(grid=True)

    # Show the line plot
    plt.show()

Here is an example of plotting a histogram:

::

    # Plot the distribution of `daily_pct_c`
    daily_pct_change.hist(bins=50)

    # Show the plot
    plt.show()

    # Pull up summary statistics
    print(daily_pct_change.describe())

We can also create a new column to store the cumulative daily returns and plot the data in a graph.

::

    # Calculate the cumulative daily returns
    cum_daily_return = (1 + daily_pct_change).cumprod()

    # Plot the cumulative daily returns
    cum_daily_return.plot(figsize=(12,8))

    # Show the plot
    plt.show()


Moving windows
---------------

**Moving windows** (also called "rolling windows") are snapshots of a portion of a time series at an instant in time. It is common
to use the moving window in a trading strategy, for example to calculate a moving average.

::

    # Isolate the closing prices 
    close_px = aapl['Close']

    # Calculate the moving average
    moving_avg = close_px.rolling(window=40).mean()

    # Inspect the result
    moving_avg.tail()

We can now easily plot the short-term and long-term moving averages:

::

    # Short moving window rolling mean
    aapl['42'] = close_px.rolling(window=40).mean()

    # Long moving window rolling mean
    aapl['252'] = close_px.rolling(window=252).mean()

    # Plot the adjusted closing price, the short and long windows of rolling means
    aapl[['Close', '42', '252']].plot()

    # Show plot
    plt.show()


Summary
-----------

#. Exploratory Data Analysis (EDA)
    * :code:`head()` and :code:`tail()` - check first or last rows
    * :code:`describe()` - mean, sd, range
    * :code:`info()` - dtype, non-null, count

#. Resampling
    * :code:`df.resample('M').mean` - downsample to months (small to big, reduce values)
    * :code:`df.resample('T').ffill()` - upsample to minutes (big to small, add values)

#. Percentage change
    * :code:`col.pct_change()`

#. Visualise data
    * :code:`col.plot` - line plot
    * :code:`col.hist(bins=50)` - histogram

#. Moving window
    * :code:`close_px.rolling(window=40).mean()` - moving average


**References**

* `Towards Data Science - What is Exploratory Data Analysis? <https://towardsdatascience.com/exploratory-data-analysis-8fc1cb20fd15>`_
* `Jason Brownlee - A Gentle Introduction to Statistical Sampling and Resampling <https://machinelearningmastery.com/statistical-sampling-and-resampling/>`_
* `Towards Data Science - Using the Pandas "Resample" Function <https://towardsdatascience.com/using-the-pandas-resample-function-a231144194c4>`_
* `Algorithmic trading explained <https://www.youtube.com/watch?v=73fnrywIhl8>`_
* `DataCamp - Python for Finance: Algorithmic Trading <https://www.datacamp.com/community/tutorials/finance-python-trading?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=255798340456&utm_targetid=aud-299261629574:dsa-473406585355&utm_loc_interest_ms=&utm_loc_physical_ms=1009279&gclid=Cj0KCQjwrIf3BRD1ARIsAMuugNu2UkliuXEzSS4V08jCIQPtBByx7Eu8tEZh0J34NJ395kpOC_t0-MUaAtF5EALw_wcB)>`_


.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.