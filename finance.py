import pandas as pd
import pandas_datareader as data
import numpy as np
import datetime
from string import ascii_uppercase
from bs4 import BeautifulSoup
from requests import get
from bokeh.plotting import show, figure, output_file
from bokeh.models.annotations import Title
from bokeh.embed import components
from bokeh.resources import CDN


URL='http://eoddata.com/stocklist/NYSE/'

#Clean up code:
#get ride of table headers code and name

def stockname(URL):
    symbol=[]
    buisness=[]
    for c in ascii_uppercase:
        url=URL+c+'.htm'
        req=get(url)
        soup=BeautifulSoup(req.text,"html.parser")
        Tab=soup.find('table',class_="quotes")
        info=Tab.find_all('tr')
        for i in range(len(info)):
            j=0
            for stig in info[i]:
                if j==0:
                    symbol.append(stig.get_text())
                elif j==1:
                    buisness.append(stig.get_text())
                else:
                    pass
                j=+1
    return(symbol,buisness)


#export to SQLlite database or csv file

#get stock info
#start and end dates
start=datetime.datetime(2020,1,1)
end=datetime.datetime(2020,11,10) #Can go a year in the past

#Buisness ID Inputs
Buis = input("Input buisness ID: ").upper()

#Buisness ID entered correctly
#https://stackoverflow.com/questions/60039161/getting-a-future-warning-when-importing-for-yahoo-with-pandas-datareader
try:
    df=data.DataReader(name=Buis, data_source="yahoo", start=start, end=end)
except:
    print('Buisness ID Incorrect. Please try again')
    while True:
        try:
            Buis = input("Input buisness ID: ")
            df=data.DataReader(name=Buis,data_source="yahoo",start=start,end=end)
            break
        except:
           print('Buisness ID Incorrect. Please try again') 

#Increasing decreasing function
def inc_dec(c,o):
    if c>o:
        value='Increase'
    elif c<o:
        value='Decrease'
    else:
        value='Equal'
    return(value)

df['Status']=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
df['Middle']=(df.Open+df.Close)/2
df['Height']=abs(df.Close-df.Open)
#filter data

p=figure(x_axis_type='datetime',height=300,width=1000, sizing_mode='scale_width')
t = Title()
t.text = Buis
p.title = t
p.grid.grid_line_alpha=0.3
h12=12*60*60*1000

p.segment(df.index,df.High,df.index,df.Low,color="black")

p.rect(df.index[df['Status']=='Increase'],df.Middle[df.Status=='Increase'],
h12,df.Height[df.Status=='Increase'],fill_color='#CCFFFF',line_color='black')

p.rect(df.index[df['Status']=='Decrease'],df.Middle[df.Status=='Decrease'],
h12,df.Height[df.Status=='Decrease'],fill_color='#FF3333',line_color='black')

website_skeleton,div1=components(p)
cdn_js=CDN.js_files
cdn_css=CDN.css_files
output_file('cs.html')
show(p)