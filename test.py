import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from difflib import get_close_matches
from difflib import SequenceMatcher
from collections import namedtuple
import pandas_datareader as data
from bs4 import BeautifulSoup
from requests import get
import yfinance as yf
from time import sleep



EW = yf.Ticker('EW')
data = EW.info  
print(data['previousClose'])
print(data['open'])
print(data['bid'],data['bidSize'])
print(data['ask'],data['askSize'])
print(data['regularMarketVolume'])
print(data['averageVolume'])
print(data['marketCap'])
print(data['beta'])
#print(data['previousClose'])
def yo():
    yesterday = datetime.today()
    period1=yesterday.replace(hour=7, minute=30).strftime('%Y-%m-%d %H:%M')
    period2=yesterday.replace(hour=14, minute=00).strftime('%Y-%m-%d %H:%M')
    yesterday1 = datetime.today().strftime('%Y-%m-%d %H:%M')


    while period1<yesterday1<period2:
        yesterday1 = datetime.today().strftime('%Y-%m-%d %H:%M')
        EW = yf.Ticker('EW')
        data = EW.info  
        print(data['regularMarketPrice'])
        sleep(60)

#dfObj = pd.DataFrame(columns=['User_ID', 'UserName', 'Action'])
#dfObj.append({'User_ID': 23, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True))