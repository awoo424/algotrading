from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime, time
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import os
import csv
import pandas as pd
dir_name= os.getcwd()+'/database_daily/'
def get_news_aastock(ticker,postfix_url,newstype,days):
        # initialize chrome setting from collecting stock using chrome driver
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument('no-sandbox')  
    chrome_options.add_argument('-disable-dev-shm-usage')  
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    driver.implicitly_wait(20)

    prefix_url='http://www.aastocks.com/en/stocks/analysis/stock-aafn/'
    try:
        SCROLL_PAUSE_TIME = 2
        fill_ticker=ticker.zfill(5)
        url=prefix_url+fill_ticker+postfix_url
        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
#         req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
#         resp = urlopen(req) 
     
        html=BeautifulSoup(driver.page_source, 'lxml')
      
        dates=html.findAll("div", {"class": "newstime4"})
        
        news=html.findAll("div", {"class": "newshead4"})
        
        idx=0
        path=os.path.join(dir_name,'data-news/'+'data-'+ticker.zfill(4)+'-aastock.csv')
        action='a'
        if (newstype=='news-daily'):
            action='w'
       

        if (len(dates)>0):
            with open(path,action) as f:
                writer = csv.writer(f)
                for i in dates:
                    
                    if "/" in str(i.get_text()):
                        date=str(i.get_text())
                        if "Release Time" in date:
                            date=date[13:23]
                        elif (date[0]==" "):
                            date=str(date[1:11])
                        else:
                            date=str(date[0:10])
                        # print(date)
                        text=news[idx].get_text()

                        date_time_obj = datetime.datetime.strptime(date, '%Y/%m/%d')
                        date_time=date_time_obj.strftime('%Y-%m-%d')
                        date_now=datetime.datetime.now().strftime('%Y-%m-%d')
                        if(datetime.datetime.now()-date_time_obj).days<=days:
                            print(text)
                            writer.writerow([date_now,text,ticker,newstype])
                        idx+=1
    except Exception as e:
        print(e)
        pass
    driver.quit()

    