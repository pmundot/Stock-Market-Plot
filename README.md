## Stock-Market-Plot

<p>
The following project while fully workson 3 different files, has yet to reach its full patential. 

The end goal for this project is to have a fully developed webpage that can drop down multipe plots
</p>

For now there are the following files:
<ul>
    <li>2 CSV files</li>
        <ul>
            <li>-All_Stocks.csv</li>
            <li>-NYSE.csv</li>
        </ul>
    <li>Finding_Stock_Exchange.py</li>
    <li>finace_interact.py</li>
    <li>finance.py</li>
    <li>cs.html</li>
</ul>

<p>
The following files work with eachother and do the following functions:
</p>
<p>
Everything is done from command prompt
</p>
<p>
<b>Finding_Stock_Exchange.py and All_Stocks.csv</b>
<ul>
    <li>use these two to find the stock exchange of your choice</li>
    <li>enter full stock exchange name Ex: New York Stock Exchange</li>
    <li>This will then scrape for all companies in that stock exchange as well as symbols</li>
    <li>it will then create a CSV of all companies and symbols for you to use</li>
    <li>This process may take some time as some exchanges have a lot of companies</li>
</ul>
</p>
<p>
<b>finace_interact.py and NYSE.csv</b>
<ul>
    <li>If you have multiple stock exchange csvs, this will find them in the same folder as file finance_interact.py</li>
    <li>NYSE.csv is a given stock exchange for the file for a person to use</li>
    <li>Will look for csv stock exchanges then look for desired company symbol wanted</li>
</ul>
</p>
<p>
<b>finance.py and cs.html</b>
<ul>
    <li>enter symbol and the code produces cs.html with company information</li>
</ul>


