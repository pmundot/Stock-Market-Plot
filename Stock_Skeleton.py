from flask import render_template, Flask, request
from datetime import datetime, timedelta
import pandas_datareader as data
from Search_Exchange import buisness, stockd, inc_dec

def date(lst):
    return(datetime(int(lst[2]),int(lst[0]),int(lst[1])))

app = Flask(__name__)
lst = {'NYSE':'New York Stock Exchange','AMEX':'American Stock Exchange','NASDAQ':'NASDAQ Stock Exchange'}
@app.route('/',methods=['GET','POST'])
def plot():
    message = ' '
    if request.method == "POST": 
       # getting input with name = fname in HTML form 
       first_name = request.form.get("fname") 
       # getting input with name = lname in HTML form  
       last_name = request.form.get("lname")  
       message =  "Your name is "+first_name + last_name 
    else:
        message = "yo fatty "
    return render_template('plot.html', message=message)

@app.route('/home/',methods=['GET','POST'])
def home():
    message=' '
    if request.method == 'GET':
        stock = request.args.get("exchange")
        if stock == ' ':
            return render_template("home.html", message = "enter exchange", lst=lst)
        try:
            company = request.args.get("company")
            start = request.args.get("start")
            end = request.args.get("end")
            time = request.args.getlist("time")
            message = stockd(date(start),date(end),'AAPL')
            return render_template("home.html", message = message, lst=lst)
        except:
            start = request.args.get("start")
            end = request.args.get("end")
            message = stockd(date(start),date(end),'AAPL')
            return render_template("home.html", message = message, lst=lst)
    return render_template("home.html", message =message, lst=lst)

@app.route('/about/',methods=['GET','POST'])
def about():
    message = ' '
    if request.method == 'GET':
        tot =request.form.get('start').split('-')
        tot1 =request.form.get('end').split('-')
        message = tot
        return render_template("about.html",message=message)
    return render_template("about.html",message=message)

    
if __name__=="__main__": #allows control over function
    app.run(debug=True) 