Sentiment analysis
===================


In this tutorial, you will learn:

* The basics in sentiment analysis
* Methods of collecting tweets
* Methods of collecting financial headlines
* What are the common ways of analyzing sentiment
* How do you measure the accuracy of the sentiment


Intro to sentiment analysis
---------------------------

| As we have discussed in the first tutorial, Sentiment analysis is a natural language processing technique used to
  determine whether data is positive, negative or neutral.
  This websites aim to explore the daily sentiment of each stock by combining financial headlines and relevant tweets,
  to find out the market sentiment.


| In the upcoming tutorial, market sentiment will be analysed through data collected from Twitter and from news article
  relevant to respective stock markets.

Collect tweets
------------------------------------


**Apply for developer account from Twitter use Tweepy**

| 1. Click and apply for a developer account through this link: https://developer.twitter.com/en/apply-for-access
| 2. Create a project and associated with developer App in the developer portal
| 3. Enable App permissions ( Read and  Write )
| 4. Navigate to 'Keys and token' page, save your API key, API secret, Access token and Access secret

Code illustration
::
    import tweepy
    # do not share the API key in any public platform (e.g github, public website)
    consumer_key = API secret
    consumer_secret = API secret
    access_token = Access token
    access_token_secret = Access secret


    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


**Access the relevant tweets using the Twitter API**

| There are different types of API provided by Twitter with various rare limitations. Please visit this link for further
  information https://developer.twitter.com/en/docs/twitter-api .In the following tutorials, you will be learning how to
  retrieve tweets from their Twitter timeline, hashtag/cashtag and also stream data that contains real time tweets.

Timeline tweets
^^^^^^^^^^^^^^^^



Hashtag/Cashtag tweets
^^^^^^^^^^^^^^^^^^^^^^^



stream tweets
^^^^^^^^^^^^^^^




Collect financial headlines
------------------------------------------

US news
^^^^^^^

| Finviz.com is a browser-based stock market research platform that allows visitors to see the latest financial news
  collected from different major newsagents such as Yahoo! finance, Accesswire, and Newsfile.

Notes
*****
Before the tutorial, it is important to a look of the front-end code of the website

.. figure:: ../images/apple_finviz_example.png

1. Access the website of each ticker through urllib.request module
::
    allnews=[]
    finviz_url = 'https://finviz.com/quote.ashx?t='
    url = finviz_url + ticker
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'})
2. Access the data from the HTML using Beautiful soup
::
    html = BeautifulSoup(resp, features="lxml")
3. Get the information of  <div> id='news-table' in the website
::
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

4. Find All the news under the <tr> tag in the news-table
::
            for info in df.findAll('tr'):
                text=info.a.get_text()
                date_scrape= info.td.text.split()
                if(len(date_scrape)==1):
                    time=date_scrape[0]
                else:
                    date= date_scrape[0]
                    time=date_scrape[1]
                    news_time_str= date+" "+time
5. Convert the date type into 'YYYY-MM-dd'
::
                date_time_obj = datetime.datetime.strptime(news_time_str, '%b-%d-%y %I:%M%p')
                date_time=date_time_obj.strftime('%Y-%m-%d')
6. Append all the news together
::
            allnews.append([date_time,text])


HK news
^^^^^^^





.. attention::
   | All investments entail inherent risk. This repository seeks to solely educate 
     people on methodologies to build and evaluate algorithmic trading strategies. 
     All final investment decisions are yours and as a result you could make or lose money.
     All final investment decisions are yours and as a result you could make or lose money.
