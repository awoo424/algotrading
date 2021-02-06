Bankruptcy prediction
==============================

In this tutorial, you will learn to:

* Train a machine learning model for bankruptcy prediction
* Carry out inferencing
* Screen out stocks based on the results


Intro to bankruptcy prediction
-------------------------------

| In this problem setting, we assume that the bankruptcy of a company could be
  predicted several years ahead. We presume that certain financial ratios are 
  significant for the prediction of bankruptcy, and that we would compute these
  ratios using the fundamentals data we have collected and train a machine learning
  model to guess if a company would go bankrupt in one year based on these financial 
  ratios.

Bankruptcy prediction with machine learning 
--------------------------------------------

| The workflow of the prediction model is outlined as follows:

1. Collect labelled data (bankrupted = 0, survived = 1)
2. Split the dataset into training set and test set a ratio of 7:3
3. Train the machine learning model(s) with the labelled data (training set)
4. Evaluate the accuracy of the training model with the test set
5. Make use of the models to predict our own set of data (i.e. inferencing)

| We will go through these steps one by one, and try to predict the bankruptcy of a set of 
  companies in Hong Kong.


Data collection
^^^^^^^^^^^^^^^^

| The labelled dataset featured in the repository is collected by the `UCLA School of Law <https://lopucki.law.ucla.edu/>`_. 
  It contains a total of about 200 records, which includes the fundamentals data of public companies in US as well as its
  bankruptcy status (bankrupted = 0, survived = 1). Note that in the suffix of the dataset file names, 
  :code:`t1` means 1 year, :code:`t2` means 2 years, and so on.

| Based on the training data and other references [1]_, the below ratios have been selected as input variables for the machine learning model:


.. math::

    X_1 &= \text{Working capital } / \text{ Total assets} \\
    X_2 &= \text{Retained earnings } / \text{ Total assets} \\
    X_3 &= \text{EBIT } / \text{ Total assets} \\
    X_4 &= \text{Total equity (book) } / \text{ Total assets} \\
    X_5 &= \text{Net income } / \text{ Total assets} \\
    X_6 &= \text{Total liabilities } / \text{ Total assets} \\


| The code snippet for concatenating the dataset and creating the variables as shown below:

::

  # Concatenate data
  data_full = pd.concat([bankrupt_data, non_bankrupt_data], ignore_index=True)

  # Add and scale variables
  data_full["X1"] = preprocessing.scale(data_full["WoCap"] / data_full["ToAsset"])
  data_full["X2"] = preprocessing.scale(data_full["CFOper"] / data_full["ToLia"])
  data_full["X3"] = preprocessing.scale(data_full["EBIT"] / data_full["ToAsset"])
  data_full["X4"] = preprocessing.scale(data_full["ToEqui"] / data_full["ToAsset"])
  data_full["X5"] = preprocessing.scale(data_full["NetInc"] / data_full["ToAsset"])
  data_full["X6"] = preprocessing.scale(data_full["ToLia"] / data_full["ToAsset"])

Train-test split
^^^^^^^^^^^^^^^^^

| The dataset is then split into training set and test set (with a ratio of 7:3), 
  so that we could achieve unbiased evaluation (i.e. the model is evaluated with fresh data).

::

  # Split data for training and testing
  X = data_full[["X1", "X2", "X3", "X4","X5","X6"]]
  y = data_full['Status'] 
  self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=101)
        


| In the example, three machine learning models typically used for classification have been chosen:

1. Support Vector Machine
2. Decision Tree
3. Random Forest
4. K-Nearest Neighbor (KNN)

| They are defined as methods of the bankruptcy prediction model class in the example file. Thus,
  it would be easier for us to compare and evaluate the performance of different machine learning
  models. 


Training the model
^^^^^^^^^^^^^^^^^^^^

::

    # after loading and pre-processing the data

    # create an instance of the class
    model = bankrupt_prediction(bankrupt_t1, non_bankrupt_t1, input_df, False)

    # train with knn
    t1_results = model.knn()


Evaluate accuracy
^^^^^^^^^^^^^^^^^

| We can check the performance of the model by looking into the confusion matrix and classification
  report:

::

  # ouput:

    Confusion Matrix using Decision Tree: 

    [[7 2]
    [2 9]]

    Classification Report using Decision Tree: 

                  precision    recall  f1-score   support

              0       0.78      0.78      0.78         9
              1       0.82      0.82      0.82        11

       accuracy                           0.80        20
      macro avg       0.80      0.80      0.80        20
   weighted avg       0.80      0.80      0.80        20


Inferencing
^^^^^^^^^^^^^^^^

| To carry out prediction with our own dataset, simply set the boolean of :code:`inferencing` to :code:`True`
  and call the method again.

::

    model.inferencing = True # set Inferencing as True

    t1_results = model.knn()

    # save results to a csv file
    t1_results.to_csv("./results/t1_results-knn.csv", header='column_names', index=False)


| To check what are the companies that survived in 1 year, load the results csv file and 
  filter out companies with a label of :code:`1`.

::

  df_t1 = pd.read_csv("./results/t1_results-knn.csv", index_col=None, header=0)
  mask = (df_t1['knn'] == 1)

  # get the percentage of survival
  len(df_t1[mask]) / len(df_t1)

| And we could save the filtered list as another csv file.

::

  df_filtered = df_t1[mask]
  df_filtered.to_csv("survived-t1.csv", header='column_names', index=False)

  



**Sources**

.. [1] SAF2002, https://ja.wikipedia.org/wiki/SAF2002

.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.