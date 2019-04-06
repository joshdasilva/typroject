from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from pprint import pprint
import pandas as pd
import wikipedia


def chart(stock, sname,wikiD):
    API_KEY = '90L3VT3DI22ZCS83'
    ts = TimeSeries(key='API_KEY', output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')

    ts2 = TechIndicators(key='API_KEY', output_format='pandas')
    data2, meta_data2 = ts2.get_bbands(symbol=stock, interval='daily', time_period=10)

    ts3 = TechIndicators(key='API_KEY', output_format='pandas')
    data3, meta_data3 = ts3.get_rsi(symbol=stock, series_type = 'close', interval='daily')

    ts4 = TechIndicators(key='API_KEY', output_format='pandas')
    data4, meta_data4 = ts4.get_macd(symbol=stock,series_type = 'close', interval='daily')

    title = 'Latest prices for Microsoft Inc.'

    data.index = pd.to_datetime(data.index)
    data2.index = pd.to_datetime(data2.index)
    data3.index = pd.to_datetime(data3.index)
    data4.index = pd.to_datetime(data4.index)


    p = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)
    p2 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)
    p3 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)
    p4 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)
    p5 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)
    p6 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)



    p.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p.line(data.index, data['4. close'], legend= stock+' price in $', line_width = 2)

    p2.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p2.line(data2.index, data2['Real Middle Band'], legend= stock+' Middle Bolinger Band$', line_width = 2)

    p3.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p3.line(data3.index, data3['RSI'], legend= stock+' RSI', line_width = 2)

    p4.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p4.line(data4.index, data4['MACD'], legend= stock+' MACD', line_width = 2)

    p5.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p5.line(data2.index, data2['Real Middle Band'], legend= stock+' combo', line_width = 2)

    p6.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p6.line(data2.index, data2['Real Middle Band'], legend= stock+' Predicted price in $', line_width = 2)

    #Store components
    script, div = components(p)
    script2, div2 = components(p2)
    script3, div3 = components(p3)
    script4, div4 = components(p4)
    script5, div5 = components(p5)
    script6, div6 = components(p6)


    #Feed them to the Django template.
    return render_to_response( 'predictx/symbols/symbol.html',
            {'script' : script , 'div' : div,'script2' : script2 , 'div2' : div2,'script3' : script3 , 'div3' : div3,'script4' : script4 , 'div4' : div4,'script5' : script5 , 'div5' : div5
             ,'script6' : script6 , 'div6' : div6, 'wiki': wikiD,'sname':sname, "stocks":Stock.objects.all})


def AlphaVantage(symbol):
    api_key=open('alpha.txt','r').read()
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol,interval='60min', outputsize='full')
    AlphaVantage('MSFT')

def indexpage(request):
    return render(request, 'predictx/index.html')

def indexpage(request):
    return render(request = request,
                  template_name='predictx/index.html',
                  context = {"stocks":Stock.objects.all})

def logout_request(request):
    logout(request)
    messages.info(request, "Succesfully Logged Out!")
    return redirect("predictx:indexpage")

#def current_stock(request):


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You're now logged in as {username}")
                return redirect('/MSFT')     #/dashboad
            else:
                messages.error(request, "Incorrect Username or Password")
        else:
            messages.error(request, "Incorrect Username or Password")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "predictx/login.html",
                    context={"form":form})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Successfully created new account: {username}")
            login(request, user)
            return redirect("predictx:indexpage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "predictx/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "predictx/register.html",
                  context={"form":form})

def MSFT(request):
    stock = 'MSFT'
    sname='Microsoft Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def AAPL(request):
    stock = 'AAPL'
    sname = 'Apple Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def AMZN(request):
    stock = 'AMZN'
    sname = 'Amazon.com Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def FB(request):
    stock = 'FB'
    sname = 'Facebook Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def BRKB(request):
    stock = 'BRK.B'
    sname = 'Berkshire Hathaway Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def GOOG(request):
    stock = 'GOOG'
    sname = 'Alphabet Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def XOM(request):
    stock = 'XOM'
    sname = 'Exxon Mobil Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def JPM(request):
    stock = 'JPM'
    sname = 'JPMorgan Chase & Co.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def V(request):
    stock = 'V'
    sname = 'Visa Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def BAC(request):
    stock = 'BAC'
    sname = 'Bank of America Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def INTC(request):
    stock = 'INTC'
    sname = 'Intel Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def CSCO(request):
    stock = 'CSCO'
    sname = 'Cisco Systems Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def VZ(request):
    stock = 'VZ'
    sname = 'Verizon Communications Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def PFE(request):
    stock = 'PFE'
    sname = 'Pfizer Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def T(request):
    stock = 'T'
    sname = 'AT&T Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def MA(request):
    stock = 'MA'
    sname = 'Mastercard Incorporated'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def BA(request):
    stock = 'BA'
    sname = 'Boeing Company'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def DIS(request):
    stock = 'DIS'
    sname = 'Walt Disney Company'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def KO(request):
    stock = 'KO'
    sname = 'Coca-Cola Company'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def PEP(request):
    stock = 'PEP'
    sname = 'PepsiCo Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def NFLX(request):
    stock = 'NFLX'
    sname = 'Netflix Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def MCD(request):
    stock = 'MCD'
    sname = 'McDonalds Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def WMT(request):
    stock = 'WMT'
    sname = 'Walmart Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def ORCL(request):
    stock = 'ORCL'
    sname = 'Oracle Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def IBM(request):
    stock = 'IBM'
    sname = 'Internation Business Machines Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def PYPL(request):
    stock = 'PYPL'
    sname = 'PalPal Holdings Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def MMM(request):
    stock = 'MMM'
    sname = '3M Company'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def NVDA(request):
    stock = 'NVDA'
    sname = 'Nvidia Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def NKE(request):
    stock = 'NKE'
    sname = 'Nike Inc.'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def COST(request):
    stock = 'COST'
    sname = 'Costco Wholesale Corporation'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

def QCOM(request):
    stock = 'QCOM'
    sname = 'Qualcomm Incorporated'
    wikiD = wikipedia.summary(sname, sentences=5)
    return chart(stock, sname, wikiD)

