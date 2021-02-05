Property Price Prediction
==========================


In this tutorial, you will learn:

* The basics in macroeconomic analysis
* The ways of analyzing macroeconomic indicators
* How to build a house price prediction model

Intro to macroeconomic analysis
-------------------------------

| As we have discussed in the first tutorial, macroeconomic analysis is a ways of
  investigating the macroeconomic indicators that influence the stock market.
  
| In this module, we will first analyze the macroeconomic indicators and explore how 
  the indicators affect the stock prices in Hong Kong. 
  
| Then, we will specifically analyze the Hong Kong real estate market, as we believe
  that it is one of the most important macroeconomic indicator that can reflect the
  Hong Kong's economy.

| In addition, we will build a house price prediction model. 

Macroeconomic indicators in Hong Kong
-------------------------------------
| Let's have a look at the data first. 


*data figure (data columns)*


Univariate analysis
^^^^^^^^^^^^^^^^^^^
| The distribution of the numerical features can be examined by calling pandas 
  Dataframe.describe() function. By calling this function, statistical summary 
  such as mean, standard deviation, min, and max of a data frame can be viewed. 

| For a better understanding of the statistics summary, seaborn.distplot() function 
  can be used to visualise the results with histograms.

  *code, figure*

Bivariate analysis
^^^^^^^^^^^^^^^^^^^
| In bivariate analysis, correlations between the features can be studied. Using 
  scatter plot and regression line, the relationship between two features were 
  visualised.

  *code, figure*

| Then, pandas.Dataframe.corr() and seaborn.heatmap() functions can be used to compute 
  a pairwise correlation of features and visualize the correlation matrix.

  *code, heatmeap*

| According to the above figure, GDP, composite consumer price index, population, 
  year, imports, month, and total exports are positively correlated to the 
  Hang Seng index, while both seasonally adjusted unemployment rate and not seasonally 
  adjusted unemployment rate are negatively correlated to the Hang Seng index.


The Hong Kong real estate market
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Under construction*

House price prediction with machine learning
--------------------------------------------

*Under construction*


.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.