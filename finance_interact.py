import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches

ET = input("Enter Stock exchange: ").title()

Exchange = pd.read_csv("All_stock.csv")
compare = Exchange["Exchange"].tolist()

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

def close_match(entry,comp):
    return(get_close_matches(entry,comp,n=3,cutoff=0.8)[0])

def close_match1(entry,comp):
    return(get_close_matches(entry,comp,n=3,cutoff=0.8)[0])

while True:
    try:
        code = get_code(ET,Exchange)
        break
    except:
        guess = close_match(ET,compare)
        res = input("did you mean {}? ".format(guess))
        if res[0].lower()=='y':
            code = get_code(guess,compare)
            break
        ET = input("Enter Stock exchange: ").title()
     
companies = pd.read_csv(code+'.csv')

CT = input("Enter Company: ").title()

while True:
    boole = companies['Company'].str.startswith(CT, na = False)
    new_comp = companies[boole]
    inter = new_comp['Company'].tolist()
    if len(inter)==0 or inter is None:
        print("Company does not exist in this stock exchange or spelling is incorrect.")
        CT = input("Enter Company: ").title()
    elif len(inter)>1:
        print("More than one company starts with that input")
        guess = close_match1(CT,inter)
        res = input("did you mean {}? ".format(guess))
        if res[0].lower()=='y':
            print(get_code1(guess,companies))
        else:
            print("Please pick from the following")
            for i in inter:
                print(i)
            CT = input("Please enter company name: ").title()
    else:
        print(get_code1(inter[0],companies))
        break

