import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import numpy as np
import argparse
import logging
import sys, os, glob
from collections import namedtuple
import difflib
from difflib import get_close_matches
from difflib import SequenceMatcher

class stock_buisness:

    def __init__(self,buis):
        self.buis = buis.title()
        self.seq = SequenceMatcher()
    
    def find_buis_exchange(self):
        exchanger = pd.read_csv('Pop_Ex.csv') 
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
        if len(style) >=1:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Analyzer")
    parser.add_argument('Command', metavar='<command>', choices = ['print'], type=str, help='command to execute: only choice is print')
    parser.add_argument('-c','--company',dest = 'company',metavar = '<company>', help= 'command to execute is a company name, check spelling')
    parser.add_argument('-s','--symbol', dest = 'symbol', metavar = '<symbol>', help= 'Enter a companies Stock symbol')
    parser.add_argument('-DS','--Start_date', dest = 'start', action = 'store', metavar = '<DS>',default = datetime.now()-timedelta(days=7), help= 'Enter date in MM-DD-YYYY format. Must be before todays date')
    parser.add_argument('-DE','--End_date', dest = 'end', action = 'store', metavar = '<ES>',default = datetime.now(), help= 'Enter date in MM-DD-YYYY format')
    parser.add_argument('-csv','--csv', dest = 'name', action = 'store', metavar = '<csv>', help= "enter a name to expot to csv")
    args = parser.parse_args()
    
    if args.company is not None and args.symbol is None:
        symbol = stock_buisness(args.company).getting_close_buis()
    elif args.company is None and args.symbol is not None:
        symbol = args.symbol
    else:
        pass

    try:
        if args.start >= datetime.now() and args.start>= args.end:
            s = input("Please enter an input that is eralier than the end date or today: ")
            start = s
        else:
            start = args.start
    except TypeError:
        s = args.start.split('-')
        start = datetime(int(s[2]),int(s[0]),int(s[1]))

    try:
        if args.end > datetime.now() and args.start>= args.end:
            e = input("Please enter an input that is later than the start date or today: ")
            end = e
        else:
            end = args.end
    except TypeError:
        e = args.end.split('-')
        start = datetime(int(e[2]),int(e[0]),int(e[1]))
    
    df=pdr.get_data_yahoo(symbol, start=start, end=end)
    df['Status']=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Close-df.Open)

    
    if args.name is not None:
        df.to_csv(args.name+'.csv')
    else:
        print(df)



    
