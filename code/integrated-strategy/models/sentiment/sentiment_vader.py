### Function for Vader Analysis 

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.downloader.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()


# read VADER scores
def read_news_vader_path(df):
    print('Reading in VADER datasets...')
    cs = []

    # append a compound score to every news row
    for row in range(len(df)):
        cs.append(analyser.polarity_scores(df['news'].iloc[row])['compound'])

    # append the column to original dataset
    df['compound_vader_score'] = cs

    return df


# group the mean compound VADER score by date
def find_news_vader_pred_label(df,threshold):
    print('Finding predicted VADER sentiment label...')

    news = df['news']
    # group the data by dates
    df = df.groupby(['dates'])['compound_vader_score'].mean().reset_index()
    final_label = []
    
    # convert the vader score using a threshold to a sentiment label
    for i in range(len(df)):

        if df['compound_vader_score'].iloc[i] > threshold:
            final_label.append(2)
        elif df['compound_vader_score'].iloc[i] < -threshold:
            final_label.append(0)
        elif (df['compound_vader_score'].iloc[i] >= -threshold  
              and df['compound_vader_score'].iloc[i] <= threshold):
            final_label.append(1)

    df['vader_label'] = final_label
    return df


# merge the dataset with the Hang Seng Index daily moving average
def merge_vader_actual_label (df,hsi_movement_df):
    print('Merging dataset with HSI daily MA...')

    vader_data = df
    vader_data.set_index(keys = ["dates"],inplace=True)
    label_data = pd.read_csv(hsi_movement_df)
    label_data.set_index(keys = ["dates"],inplace=True)

    # inner join the two datasets using the date index
    merge = pd.merge(vader_data,label_data, how='inner', left_index=True, right_index=True)
    merge = merge.reset_index()

    # drop the redudant column 
    merge = merge.drop(['Unnamed: 0'],axis=1)
    
    return merge

### Starter function for VADER sentiment analysis ###
def starter_vader(path,result_path):
    # get the full path of each ticker
    df = pd.read_csv(path,names=['dates','news','ticker','newstype'])

    # read append the compound vader score to the pandas dataframe
    df = read_news_vader_path(df)

    # pass in the threshold to get the vader label
    df = find_news_vader_pred_label(df,0.01)

    # store to the csv file if the dataset is not empty
    df = df.drop('compound_vader_score',axis=1)

    if (df.empty == False): # if df not empty
        df.to_csv(result_path,index=False)

    return df

