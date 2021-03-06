from flask import render_template, Flask, request, flash
import pandas as pd
from datetime import datetime, timedelta
from pandas_datareader import data as pdr
from Search_Exchange import buisness, stockd, inc_dec, stock_plot, add_class


app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def home():
    start = datetime.now()
    end = start - timedelta(days=7)
    if request.method == 'GET':
        try:
            start = request.args.get("start")
            end = request.args.get("end")
            company = request.args.get("company")
            df=stockd(start,end,company).sort_values(by='Date',ascending=False)
        except:
            end = datetime.now()
            start = end - timedelta(days=7) 
            company = 'A'
            df=stockd(start,end,company).sort_values(by='Date',ascending=False)
        plots = stock_plot(df,company.upper())
        df = df[['High','Low','Open','Close','Status']].round(2)
        df = add_class(df)
        dt = {'price':98.60, 'company':'edwards', 'prec':33}
        print(df)
        return render_template("home.html", link = plots[2], the_div=plots[0], the_script=plots[1], tables=df, message=dt)
    return render_template("home.html", link = plots[2], the_div=plots[0], the_script=plots[1], message=dt)

@app.route('/about/',methods=['GET','POST'])
def about():
    data = pd.read_csv('stock_market//Pop_Ex.csv')
    if request.method == 'GET':
        try:
            company = request.args.get("company").title()
        except:
            company = "A"
        data = data.loc[data['Company'].str.startswith(company, na=False)]
        exchanges = request.args.getlist('ex')
        if len(exchanges)!=0:
            data = data[data['Ex Code'].isin(exchanges)]
            data = data[['Code','Company','Exchange','Ex Code']]
        return render_template("about.html",tables=[data.to_html(classes='data')])
    return render_template("about.html",tables=[data.to_html(classes='data')])

    
if __name__=="__main__": #allows control over function
    app.run(debug=True) 

