import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from difflib import get_close_matches
from difflib import SequenceMatcher
from collections import namedtuple
import pandas_datareader as data
#from Search_Exchange import exchange

All_S = pd.read_csv('Stock_Market\\All_stock.csv')
symbols = All_S['Code'].tolist()
exchanges = All_S['Exchange'].tolist()
letters = All_S['Letters'].tolist()
seq = SequenceMatcher()

search = "Neeew Yrk Stock"

def getting_close(name):
    S = len(name.split())
    new_list = [' '.join((c.split())[:S]) for c in exchanges]
    still = []
    for i,c in enumerate(new_list):
        seq.set_seqs(name,c)
        d = seq.ratio()
        if d>0.9: 
            still.append(i)
    return(still[0])


def redundant_getting_close(name):
    S = len(name.split())
    new_list = [' '.join((c.split())[:S]) for c in exchanges]
    return(get_close_matches(name,new_list,n=4,cutoff=0.8)[0])

def stop(yo):
    print(exchange(yo).get_code())
    while True:
        try:
            print(exchanges[getting_close(yo)])
            break
        except IndexError:
            question=input("did you mean {}?: ".format(redundant_getting_close(search)))
            if question[0].lower()=='y':
                search = redundant_getting_close(search)
            else:
                search = input("Input new stock exchange: ")


def create(x,y,z):
    orig = datetime(x,y,z)
    orig = str(orig)
    d = datetime.strptime(orig, '%Y-%m-%d')
    d = d.strftime('%m/%d/%y')
    return(d)

print(create(1948,9,12))
