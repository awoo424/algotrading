import os 
import pandas as pd
from textblob import TextBlob

# !pip install textblob

# append the normalised textblob (-1 to 1) score to the corresponding news
def read_news_textblob_path(df):

    print('Reading in TextBlob sentiment datasets...')
    cs = []

    # append a compound score to every news row
    for row in range(len(df)):
        cs.append(TextBlob(df['news'].iloc[row]).sentiment[0])

    # append the column to original dataset
    df['compound_textblob_score'] = cs

    return df


# group the mean compound textblob score by date
def find_news_textblob_pred_label(df, threshold):
    print('Finding predicted label...')
    news = df['news']

    # group the data by dates
    df = df.groupby(['dates'])['compound_textblob_score'].mean().reset_index()
    final_label = []
    
    # convert the VADER score using a threshold to a sentiment label
    for i in range(len(df)):

        if df['compound_textblob_score'].iloc[i] > threshold:
            final_label.append(2)
        elif df['compound_textblob_score'].iloc[i] < -threshold:
            final_label.append(0)
        elif (df['compound_textblob_score'].iloc[i] >= -threshold  
              and df['compound_textblob_score'].iloc[i] <= threshold):
            final_label.append(1)

    df['textblob_label'] = final_label

    return df

# merge the dataset with the Hang Seng Index daily moving average
def merge_textblob_actual_label (df,hsi_movement_df):

    print('Merging dataset with HSI daily MA...')
    textblob_data = df
    textblob_data.set_index(keys = ["dates"],inplace=True)
    label_data = pd.read_csv(hsi_movement_df)
    label_data.set_index(keys = ["dates"],inplace=True)

    # inner join the two datasets using the date index
    merge = pd.merge(textblob_data,label_data, how='inner', left_index=True, right_index=True)
    merge = merge.reset_index()

    # drop the redundant column 
    merge = merge.drop(['Unnamed: 0'],axis=1)
    
    return merge


### Starter function for textblob sentiment analysis ###
def starter_textblob(path,result_path):
          
    df = pd.read_csv(path,names=['dates','news','ticker','newstype'])

    # read append the compound vader score to the pandas dataframe
    df = read_news_textblob_path(df)

    # pass in the threshold to get the vader label
    df = find_news_textblob_pred_label(df, 0.01)
    
    db_df = pd.read_csv(result_path)

    if (df['textblob_label'].any()):
        db_df['textblob_label'] = df['textblob_label']
    else:
        db_df['textblob_label'] = 0

    # store to the csv file if the dataset is not empty
    if (db_df.empty == False):
        db_df.to_csv(result_path,index=False)

    return db_df