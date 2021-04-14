Integrated trading strategy
==================================

In this tutorial, you will learn:

* How to make use of different features to write a strategy
* How to use machine learning models to predict trading signals

.. highlight:: Python

Putting it all together
----------------------------

| In this part we'll look into how to put everything together in order to build a strategy that
  incorporates different features (technical indicator, macroeconomic trends and sentiment indicator) so as to
  comprehensively examine the market as a whole.


Simple approach
-------------------

| We'll first look into simplistic, rule-based methods to make use of the features in an 
  algorithmic trading pipeline.

Baseline model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The implementation of the baseline model could be found in :code:`integrated-strategy/baseline.py`.

| *WIP*

Machine learning approach
--------------------------------------

| Moving on, we'll look into more advanced methods that pass the data features into a machine learning model
  in order to make sequential predictions.

Recurrent Neural Networks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A **recurrent neural network (RNN)** is a type of artificial neural network designed for sequential data or time series data.
  As opposed to traditional feedforward neural networks, they are networks with loops in them which allow information to persist.
  It has a lot of applications, ranging from language modelling to speech recognition. You can read more about the it in Andrej
  Karpathy's blog post - `The Unreasonable Effectiveness of Recurrent Neural Networks <http://karpathy.github.io/2015/05/21/rnn-effectiveness/>`_. 

| However, one problem with RNNs is that they have a hard time in capturing long-term dependencies. When making a prediction at the
  current time step, RNNs would weigh more recent historical information to be more important. But sometimes contextual information could
  lie in the far past. This is When LSTM comes into play.

.. role:: raw-html(raw)
  :format: html

.. figure:: ../images/LSTM.png
  :width: 500px
  :align: center
  :height: 190px
  :alt: "LSTM model."

  :raw-html:`<br/>`
  The internal structure of an LSTM. [1]_


| **Long Short Term Memory networks (LSTMs)** is an improved version of RNN that is specifically designed to avoid the long-term dependency problem.
  Their default behaviour is to remember information for long periods of time.

| If you want to know more about the mechanism and details of LSTMs, you could read this great blog post - 
  `Understanding LSTM Networks <https://colah.github.io/posts/2015-08-Understanding-LSTMs/#:~:text=Long%20Short%20Term%20Memory%20networks,many%20people%20in%20following%20work.>`_


Single-feature LSTM model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The implememtation of the single-feature LSTM model could be found in :code:`integrated-strategy/LSTM-train_price-only.py`.

| *WIP*

Multi-feature LSTM model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The implememtation of the single-feature LSTM model could be found in :code:`integrated-strategy/LSTM-train_wrapper.py`.

| *WIP*

**References**

* `Understanding LSTM Networks <https://colah.github.io/posts/2015-08-Understanding-LSTMs/>`_
* `Long Short Term Memory <http://www.bioinf.jku.at/publications/older/2604.pdf>`_


**Image sources**

.. [1] By Christopher Olah - Understanding LSTM Networks, https://colah.github.io/posts/2015-08-Understanding-LSTMs


.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.