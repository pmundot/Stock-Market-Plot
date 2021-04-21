import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import sys
import os
import datetime
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

class exchange:
    def __init__(self,search):
        self.All_S = pd.read_csv('All_stock.csv')
        self.symbols = self.All_S['Code'].tolist()
        self.exchanges = self.All_S['Exchange'].tolist()
        self.letters = self.All_S['Letters'].tolist()
        self.seq = SequenceMatcher()
        self.URL='http://eoddata.com/stocklist/'
        self.search = search.title()
    
    def get_code(self):
        while True:
            try:
                return(self.symbols[self.getting_close()])
                break
            except IndexError:
                question=input("did you mean {}?: ".format(self.redundant_getting_close()))
                if question[0].lower()=='y':
                    self.search = self.redundant_getting_close()
                else:
                    self.search = input("Input new stock exchange: ")
    
    def getting_close(self):
        S = len(self.search.split())
        new_list = [' '.join((c.split())[:S]) for c in self.exchanges]
        still = []
        for i,c in enumerate(new_list):
            self.seq.set_seqs(self.search,c)
            d = self.seq.ratio()
            if d>0.9: 
                still.append(i)
        self.still = still
        return(self.still[0])


    def redundant_getting_close(self):
        S = len(self.search.split())
        new_list = [' '.join((c.split())[:S]) for c in self.exchanges]
        return(get_close_matches(self.search,new_list,n=4,cutoff=0.8)[0])

    def stockname(self):
        self.code = []
        self.buisness = []
        fort = self.getting_close()
        for c in self.letters[fort]:
            url=self.URL+self.symbols[fort]+'/'+c+'.htm'
            req=get(url)
            soup=BeautifulSoup(req.text,"html.parser")
            Tab=soup.find('table',class_="quotes")
            info=Tab.find_all('tr')
            for i in range(len(info)):
                poper = info[i].find_all('td')
                for j in range(len(poper)):
                    if j==0:
                        self.code.append(poper[0].get_text())
                    if j==1:
                        self.buisness.append(poper[1].get_text())
        exchange = pd.DataFrame()
        exchange['Code'] = self.code
        exchange['Company'] = self.buisness
        exchange['Exchange'] = [self.exchanges[self.getting_close()] for i in self.code ]
        exchange['Ex Code'] = [self.symbols[self.getting_close()] for i in self.code ]
        exchange.to_csv(self.symbols[self.getting_close()]+'.csv')

    def run(self):
        return(self.get_code())
    
    
class buisness:

    def __init__(self,buis):
        self.buis = buis.title()
        self.search = input('Enter Stock Exchange: ')
        self.seq = SequenceMatcher()
    
    def find_buis_exchange(self):
        self.exfile = exchange(self.search).run()
        exchanger = pd.read_csv(self.exfile+'.csv') 
        self.symbols = exchanger['Code'].tolist()
        self.companies = exchanger['Company'].tolist()

    def getting_close_buis(self):
        self.find_buis_exchange()
        while True:
            S = len(self.buis.split())
            new_list = [' '.join((str(c).split())[:S]) for c in self.companies]
            Number = new_list.count(self.buis)
            if Number > 1:
                self.buis = input("There are {} results matching this name. Please enter the total name of the company: ".format(Number)).title()
            else:
                pass
            try:
                indexing = new_list.index(self.buis)
                break
            except ValueError:
                answer = input("Did you mean {} (y/n): ".format(self.redundant_getting_close()))
                if answer[0].lower() == 'y':
                    self.buis = self.redundant_getting_close()
                else:
                    self.buis = input('Please enter another company: ')
        return(self.symbols[indexing])

    def redundant_getting_close(self):
        self.find_buis_exchange()
        S = len(self.buis.split())
        new_list = [' '.join((str(c).split())[:S]) for c in self.companies]
        style = get_close_matches(self.buis,new_list,n=4,cutoff=0.8)[0]
        if style >=1:
            return(style)
        else:
            return('Company does not exists in this exchange')

    def run(self):
        try:
            return(self.getting_close_buis())
        except FileNotFoundError:
            exchange(self.search).stockname()
            return(self.getting_close_buis())

class Flask_buisness:

    def __init__(self,buis):
        self.buis = buis.title()
        self.seq = SequenceMatcher()
    
    def find_buis_exchange(self):
        self.exchanger = pd.read_csv('Exchanges.csv') 
        self.symbols = self.exchanger['Code'].tolist()
        self.companies = self.exchanger['Company'].tolist()

    def getting_close_buis(self):
        self.find_buis_exchange()
        while True:
            S = len(self.buis.split())
            new_list = [' '.join((str(c).split())[:S]) for c in self.companies]
            Number = new_list.count(self.buis)
            if Number > 1:
                self.buis = input("There are {} results matching this name. Please enter the total name of the company: ".format(Number)).title()
            else:
                pass
            try:
                indexing = new_list.index(self.buis)
                break
            except ValueError:
                answer = input("Did you mean {} (y/n): ".format(self.redundant_getting_close()))
                if answer[0].lower() == 'y':
                    self.buis = self.redundant_getting_close()
                else:
                    self.buis = input('Please enter another company: ')
        return(self.symbols[indexing])

    def redundant_getting_close(self):
        self.find_buis_exchange()
        S = len(self.buis.split())
        new_list = [' '.join((str(c).split())[:S]) for c in self.companies]
        style = get_close_matches(self.buis,new_list,n=4,cutoff=0.8)[0]
        if style >=1:
            return(style)
        else:
            return('Company does not exists in this exchange')


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

def stock_plot(df,comp):
    p=figure(x_axis_type='datetime',height=300,width=1000, sizing_mode='scale_width')
    t = Title()
    t.text = comp
    p.title = t
    p.grid.grid_line_alpha=0.3
    h12=12*60*60*1000
    curdoc().theme = "dark_minimal"
    p.segment(df.index,df.High,df.index,df.Low,color="black")

    p.rect(df.index[df['Status']=='Increase'],df.Middle[df.Status=='Increase'],
        h12,df.Height[df.Status=='Increase'],fill_color='lime',line_color='black')

    p.rect(df.index[df['Status']=='Decrease'],df.Middle[df.Status=='Decrease'],
        h12,df.Height[df.Status=='Decrease'],fill_color='red',line_color='black')
    web,div1=components(p)
    cdn_js=CDN.js_files[0]
    return(web,div1,cdn_js)

