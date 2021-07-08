import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime
import numpy as np
import sys
import os
from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup
from requests import get
import difflib
from difflib import get_close_matches
from difflib import SequenceMatcher
from bokeh.plotting import show, figure, output_file
from bokeh.models.annotations import Title
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.io import curdoc

def inc_dec(c,o):
    if c>o:
        value='Increase'
    elif c<o:
        value='Decrease'
    else:
        value='Equal'
    return(value)

def stockd(start,end,buisness):
    df=pdr.get_data_yahoo(buisness, start=start, end=end)
    df['Status']=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Close-df.Open)
    return(df)
start = datetime(2021,2,1)
end = datetime(2021,2,7)
print(stockd(start,end,'EW'))