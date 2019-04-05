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


def MSFT(request):
    stock = 'MSFT'
    wikiD = wikipedia.summary("microsoft", sentences=5)
    return chart(stock, wikiD)

def AAPL(request):
    return render(request = request,
                  template_name='predictx/symbols/AAPL.html',
                  context = {"stocks":Stock.objects.all})

def chart(stock, wikiD):
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
    return render_to_response( 'predictx/symbols/'+stock+'.html',
            {'script' : script , 'div' : div,'script2' : script2 , 'div2' : div2,'script3' : script3 , 'div3' : div3,'script4' : script4 , 'div4' : div4,'script5' : script5 , 'div5' : div5
             ,'script6' : script6 , 'div6' : div6, 'wiki': wikiD, "stocks":Stock.objects.all})


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
                return redirect('/AAPL')     #/dashboad
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


def AAPL(request):
    return render(request, 'predictx/symbols/AAPL.html')

def AAPL(request):
    return render(request = request,
                  template_name='predictx/symbols/AAPL.html',
                  context = {"stocks":Stock.objects.all})

def AMZN(request):
    return render(request = request,
                  template_name='predictx/symbols/AMZN.html',
                  context = {"stocks":Stock.objects.all})
def FB(request):
    return render(request = request,
                  template_name='predictx/symbols/FB.html',
                  context = {"stocks":Stock.objects.all})
def BRKB(request):
    return render(request = request,
                  template_name='predictx/symbols/BRKB.html',
                  context = {"stocks":Stock.objects.all})
def GOOG(request):
    return render(request = request,
                  template_name='predictx/symbols/GOOG.html',
                  context = {"stocks":Stock.objects.all})
def XOM(request):
    return render(request = request,
                  template_name='predictx/symbols/XOM.html',
                  context = {"stocks":Stock.objects.all})
def JPM(request):
    return render(request = request,
                  template_name='predictx/symbols/JPM.html',
                  context = {"stocks":Stock.objects.all})
def V(request):
    return render(request = request,
                  template_name='predictx/symbols/V.html',
                  context = {"stocks":Stock.objects.all})
def BAC(request):
    return render(request = request,
                  template_name='predictx/symbols/BAC.html',
                  context = {"stocks":Stock.objects.all})
def INTC(request):
    return render(request = request,
                  template_name='predictx/symbols/INTC.html',
                  context = {"stocks":Stock.objects.all})
def CSCO(request):
    return render(request = request,
                  template_name='predictx/symbols/CSCO.html',
                  context = {"stocks":Stock.objects.all})
def VZ(request):
    return render(request = request,
                  template_name='predictx/symbols/VZ.html',
                  context = {"stocks":Stock.objects.all})
def PFE(request):
    return render(request = request,
                  template_name='predictx/symbols/PFE.html',
                  context = {"stocks":Stock.objects.all})
def T(request):
    return render(request = request,
                  template_name='predictx/symbols/T.html',
                  context = {"stocks":Stock.objects.all})
def MA(request):
    return render(request = request,
                  template_name='predictx/symbols/MA.html',
                  context = {"stocks":Stock.objects.all})
def DIS(request):
    return render(request = request,
                  template_name='predictx/symbols/DIS.html',
                  context = {"stocks":Stock.objects.all})
def KO(request):
    return render(request = request,
                  template_name='predictx/symbols/KO.html',
                  context = {"stocks":Stock.objects.all})
def PEP(request):
    return render(request = request,
                  template_name='predictx/symbols/PEP.html',
                  context = {"stocks":Stock.objects.all})
def NFLX(request):
    return render(request = request,
                  template_name='predictx/symbols/NFLX.html',
                  context = {"stocks":Stock.objects.all})
def MCD(request):
    return render(request = request,
                  template_name='predictx/symbols/MCD.html',
                  context = {"stocks":Stock.objects.all})
def WMT(request):
    return render(request = request,
                  template_name='predictx/symbols/WMT.html',
                  context = {"stocks":Stock.objects.all})
def ORCL(request):
    return render(request = request,
                  template_name='predictx/symbols/ORCL.html',
                  context = {"stocks":Stock.objects.all})
def IBM(request):
    return render(request = request,
                  template_name='predictx/symbols/IBM.html',
                  context = {"stocks":Stock.objects.all})
def PYPL(request):
    return render(request = request,
                  template_name='predictx/symbols/PYPL.html',
                  context = {"stocks":Stock.objects.all})
def NVDA(request):
    return render(request = request,
                  template_name='predictx/symbols/NVDA.html',
                  context = {"stocks":Stock.objects.all})
def NKE(request):
    return render(request = request,
                  template_name='predictx/symbols/NKE.html',
                  context = {"stocks":Stock.objects.all})
def COST(request):
    return render(request = request,
                  template_name='predictx/symbols/COST.html',
                  context = {"stocks":Stock.objects.all})
def QCOM(request):
    return render(request = request,
                  template_name='predictx/symbols/QCOM.html',
                  context = {"stocks":Stock.objects.all})

