Data science basics
======================

.. highlight:: Julia

In this tutorial, you will learn to do the following in Julia:

* Load and output csv files
* Manipulate DataFrames

You could run the code for this tutorial in :code:`code/technical-analysis_julia/data-science-basics.ipynb`. 
Make sure you have installed Julia and all the required dependencies (follow instructions `here <https://github.com/JuliaLang/julia>`_). 


You would need to install and import the following libraries:

::

  # import libraries
  using CSV;
  using Dates;
  using DataFrames;
  using Statistics;
  using Plots;
  using StatsPlots;
  using RollingFunctions;


Read and output csv file
--------------------------

The CSV package is useful for loading and manipulating dataframes.

::

  # load data
  df = CSV.File("../../database/hkex_ticks_day/hkex_0001.csv") |> DataFrame

::

  # save as csv
  CSV.write("test.csv", df)


Data inspection
--------------------------


The :code:`first` and :code:`last` functions are similar to :code:`head` and :code:`tail`
in pandas. Additionally, we also have :code:`describe` that returns a summary of the dataframe.

::

  first(df, 5) # show first 5 rows
  last(df, 5) # last 5 rows


::

  describe(df) # get summary of df


We can get the column names by:

::

  names(df) # column names


Data selection
--------------------------


As we always select rows within a particular date range for stock price data, here is how to do it:

::

  df[(df.Date .> Date(2017, 1)) .& (df.Date .< Date(2019, 1)), :]

Alteratively, we could generate a list of dates and check if date is in this range:

::

  dates = [Date(2017, 1),Date(2018)];
  yms = [yearmonth(d) for d in dates];
  print(yms) # [(2017, 1), (2018, 1)]

  df[in(yms).(yearmonth.(df.Date)), :], 10


We can select column(s) by the following way:

::

  close = select(df, :Close) # select column "Close"
  close = select(df, [:Close, :Volume]) # select columns "Close", "Volume"



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