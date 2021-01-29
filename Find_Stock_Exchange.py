import pandas as pd
import numpy as np
import datetime
from collections import namedtuple
from string import ascii_uppercase
from bs4 import BeautifulSoup
from requests import get
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches

All_S = pd.read_csv('All_stock.csv')

symbols = All_S['Code'].tolist()
exchanges = All_S['Exchange'].tolist()
letters = All_S['Letters'].tolist()

def get_code(entry,df):
    info  = namedtuple('info','symbol lst pos')
    if entry in df['Exchange'].tolist():
        pos_ex = df[df['Exchange']==entry].index.item()
        symb = df['Code'].iloc[int(pos_ex)]
        letters = df['Letters'].iloc[int(pos_ex)]
    return(info(symb,letters,pos_ex))

def close_match(entry):
    return(get_close_matches(entry,exchanges,n=3,cutoff=0.8)[0])

def stockname(URL,sym,lst):
    symbol = []
    buisness = []
    for c in lst:
        url=URL+sym+'/'+c+'.htm'
        req=get(url)
        soup=BeautifulSoup(req.text,"html.parser")
        Tab=soup.find('table',class_="quotes")
        info=Tab.find_all('tr')
        for i in range(len(info)):
            poper = info[i].find_all('td')
            for j in range(len(poper)):
                if j==0:
                    symbol.append(poper[0].get_text())
                if j==1:
                    buisness.append(poper[1].get_text())

    return(symbol,buisness)

URL='http://eoddata.com/stocklist/'

ET = input("Enter Stock exchange: ").title()

while True:
    try:
        code=get_code(ET,All_S)
        break
    except:
        guess = close_match(ET)
        res = input("did you mean {}? ".format(guess))
        if res[0].lower()=='y':
            code = get_code(guess,All_S)
            break
        ET = input("Enter Stock exchange: ").title()


tom,jerry = stockname(URL,code.symbol,code.lst)

exchange = pd.DataFrame()
exchange['Code'] = tom
exchange['Company'] = jerry
exchange['Exchange'] = [exchanges[code.pos] for i in tom ]
exchange['Ex Code'] = [symbols[code.pos] for i in tom ]
exchange.to_csv(symbols[code.pos]+'.csv')