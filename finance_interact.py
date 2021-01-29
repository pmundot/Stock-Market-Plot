import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches

ET = input("Enter Stock exchange: ").title()

compare = pd.read_csv("All_stock.csv")
get_close = compare["Exchange"].tolist()

def get_code(entry,df):
    if entry in df['Exchange'].tolist():
        pos_ex = df[df['Exchange']==entry].index.item()
        symb = df['Code'].iloc[int(pos_ex)]
    return(symb)

def get_code1(entry,df):
    if entry in df['Company'].tolist():
        pos_ex = df[df['Company']==entry].index.item()
        symb = df['Code'].iloc[int(pos_ex)]
    return(symb)

def close_match(entry):
    return(get_close_matches(entry,get_close,n=3,cutoff=0.8)[0])

def close_match1(entry):
    return(get_close_matches(entry,get_close,n=3,cutoff=0.8))

while True:
    try:
        code = get_code(ET,compare)
    except:
        guess = close_match(ET)
        res = input("did you mean {}? ".format(guess))
        if res[0].lower()=='y':
            code = get_code(guess,compare)
            break
        ET = input("Enter Stock exchange: ").title()
     
companies = pd.read_csv(code+'.csv')
get_close = companies['Company'].tolist()

CT = 'Edwards'#input("Enter Company: ")

#while True:
#    try:
#        code1 = get_code1(CT,companies)
#    except:
#        guess = close_match(CT)
#        res = input("did you mean {}? ".format(guess))
#        if res[0].lower()=='y':
#            code1 = get_code1(guess,companies)
#            break
#        CT = input("Enter company (company may not be in this stock exchange): ").title()

#print(code1)