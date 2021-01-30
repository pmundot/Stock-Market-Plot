# Stock-Market-Plot

The following project while fully workson 3 different files, has yet toreach its full patential. 

The end goal for this project is to have a fully developed webpage that can drop down multipe plots

For now there are the following files:
-2 CSV files
---All_Stocks.csv
---NYSE.csv
-Finding_Stock_Exchange.py
-finace_interact.py
-finance.py
-cs.html

The following files work with eachother and do the following functions:

Everything isdone from command prompt

<b>Finding_Stock_Exchange.py and All_Stocks.csv</b>
-use these two to find the stock exchange of your choice
-enter full stock exchange name Ex: New York Stock Exchange
-This will then scrape for all companies in that stock exchange as well as symbols
-it will then create a CSV of all companies and symbols for you to use
-This process may take some time as some exchanges have a lot of companies

finace_interact.py and NYSE.csv:
-If you have multiple stock exchange csvs, this will find them in the same folder as file finance_interact.py
-NYSE.csv is a given stock exchange for the file for a person to use
-Will look for csv stock exchanges then look for desired company symbol wanted

finance.py and cs.html
-enter symbol and the code produces cs.html with company information


