from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from math import pi
from bokeh.layouts import row, column, gridplot
from bokeh.plotting import figure, output_file, show, curdoc, _figure
from bokeh.embed import components
from bokeh.driving import count
from bokeh.models import DatetimeTickFormatter,HoverTool, ColumnDataSource, Slider, Select, BasicTickFormatter
from pprint import pprint
import pandas as pd
import wikipedia, os

def chart(stock, sname, wikiD):

    API_KEY = 'ZCXPM8FMBJXNOE3J'
    ts = TimeSeries(key='API_KEY', output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='full')

    ts2 = TechIndicators(key='API_KEY', output_format='pandas')
    data2, meta_data2 = ts2.get_bbands(symbol=stock, interval='daily', time_period=10)

    ts3 = TechIndicators(key='API_KEY', output_format='pandas')
    data3, meta_data3 = ts3.get_rsi(symbol=stock, series_type = 'close', interval='daily')

    ts4 = TechIndicators(key='API_KEY', output_format='pandas')
    data4, meta_data4 = ts4.get_macd(symbol=stock,series_type = 'close', interval='daily')

    title = 'Latest prices for'+sname

    data.index = pd.to_datetime(data.index)
    data2.index = pd.to_datetime(data2.index)
    data3.index = pd.to_datetime(data3.index)
    data4.index = pd.to_datetime(data4.index)

    long_rolling = data['5. adjusted close'].rolling(window=200).mean()
    short_rolling = data['5. adjusted close'].rolling(window=20).mean()
    ema_short = data['5. adjusted close'].ewm(span=20, adjust=False).mean()
    ema_long = data['5. adjusted close'].ewm(span=200, adjust=False).mean()



    latest = data.tail(1)
    lOpen = latest.iloc[:, 0:1].values
    lHigh = latest.iloc[:, 1:2].values
    lLow = latest.iloc[:, 2:3].values
    lClose = latest.iloc[:, 3:4].values
    lAdjClose = latest.iloc[:, 4:5].values
    lVol = latest.iloc[:, 5:6].values
    lDiv = latest.iloc[:, 6:7].values
    lSplit = latest.iloc[:, 7:8].values

    # lOpen = latest['1. open']
    # lHigh = latest['2. high']
    # lLow = latest['3. low']
    # lClose = latest['4. close']
    # lAdjClose = latest['5. adjusted close']
    # lVol = latest['6. volume']
    # lDiv = latest['7. dividend amount']
    # lSplit = latest['8. split coefficient']

    source1 = ColumnDataSource(data=dict(x=data.index, y=data['5. adjusted close'], ssma=short_rolling, lsma=long_rolling, sema=ema_short,lema=ema_long))
    source2 = ColumnDataSource(data=dict(x = data.index, z=data['4. close'], bu=data2['Real Upper Band'], bm=data2['Real Middle Band'], bl=data2['Real Lower Band']))
    source3 = ColumnDataSource(data=dict(x = data.index, x2= data3.index,  z=data['4. close'], rsi = data3['RSI']))
    source4 = ColumnDataSource(data=dict(x = data.index, x2 = data4.index, z=data['4. close'], macd=data4['MACD'], macds = data4['MACD_Signal']))
    source5 = ColumnDataSource(data=dict(x = data.index, y=data['5. adjusted close']))



    p = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,)
    p1 = figure(title= title ,
        x_axis_label= 'date',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset']
                )
    p1.add_tools(HoverTool(tooltips=[("Date", "@x{%F}"), ("20 day SMA", "@ssma{%0.2f}"), ("200 day SMA", "@lsma{%0.2f}"), ("20 day EMA", "@sema{%0.2f}"), ("200 day EMA", "@lema{%0.2f}")],
        formatters={
            'x': 'datetime',
            'ssma': 'printf',
            'lsma': 'printf',
            'sema': 'printf',
            'lema': 'printf'
        },
        mode='vline'))

    p2 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset']
                )
    p2.add_tools(HoverTool(tooltips=[("Date", "@x{%F}"), ("Close", "@z{%0.2f}"), ("Real Upper Band", "@bu{%0.2f}"), ("Real Middle Band", "@bm{%0.2f}"), ("Real Lower Band", "@bl{%0.2f}")],
        formatters={
            'x': 'datetime',
            'z': 'printf',
            'bu': 'printf',
            'bm': 'printf',
            'bl': 'printf'
        },
        mode='vline'))
    p3 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset']
                )
    p35 = figure(plot_height=250, plot_width = 1300, x_range=p3.x_range, y_axis_location="right", x_axis_type="datetime")
    p3.add_tools(HoverTool(tooltips=[("Date", "@x{%F}"), ("Close", "@z{%0.2f}"), ("RSI", "@rsi{%0.2f}")],
        formatters={
            'x': 'datetime',
            'z': 'printf',
            'rsi': 'printf'
        },
        mode='vline'))

    p4 = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset']
                )
    p45 = figure(plot_height=250, plot_width = 1300,  x_range=p4.x_range, y_axis_location="right", x_axis_type="datetime")
    p4.add_tools(HoverTool(tooltips=[("Date", "@x{%F}"), ("Close", "@z{%0.2f}"), ("MACD", "@macd{%0.2f}"), ("MAC Signal", "@macds{%0.2f}")],
                               formatters={
                                   'x': 'datetime',
                                   'z': 'printf',
                                   'macd': 'printf',
                                   'macds': 'printf',
                                   'macdh': 'printf'
                               },
                               mode='vline'))


    p5 = figure( title= title ,
        x_axis_label= 'Date',
        x_axis_type="datetime",
        y_axis_label= 'Close Price',
        plot_width =1300,
        plot_height =600,
        tools = ['pan', 'wheel_zoom', 'box_zoom','reset']
    )
    p5.add_tools(HoverTool(tooltips=[
        ("(Date:, Adjusted Close:)", "(@x{%F}, @y{%0.2f})"),
    ],
        formatters={
            'x': 'datetime',
            'y': 'printf',
        },
        mode='vline')
    )

    p55 = figure(plot_height=140, plot_width=1300, x_range=p5.x_range, x_axis_type="datetime", y_axis_location="right")
    p55.yaxis.formatter = BasicTickFormatter(use_scientific=False)


    p6 = figure(title= title ,
        x_axis_label= 'Days',
        #x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600)

    cdata = data.tail(310)
    inc = cdata['4. close'] > cdata['1. open']
    dec = cdata['1. open'] > cdata['4. close']
    w = 12 * 60 * 60 * 1000  # half day in ms
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    p.segment(cdata.index, cdata['2. high'], cdata.index, cdata['3. low'], color="black")
    p.vbar(cdata.index[inc], w, cdata['1. open'][inc], cdata['4. close'][inc], fill_color="#7cfc00", line_color="black")
    p.vbar(cdata.index[dec], w, cdata['1. open'][dec], cdata['4. close'][dec], fill_color="#ff0000", line_color="black")


    p1.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p1.line('x','y', legend= stock+' price in $', line_width = 2,color='blue', muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'lsma', legend= stock+' 200 day MA', line_width = 2, color ='red',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'ssma', legend= stock+' 20 day MA', line_width = 2, color ='yellow',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'lema', legend= stock+' 200 day EMA', line_width = 2, color ='green',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'sema', legend= stock+' 20 day MA', line_width = 2, color ='orange',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.legend.location = "top_left"
    p1.legend.click_policy = "mute"

    p2.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p2.line('x', 'z', legend= stock+' price in $', line_width = 2, color ='blue', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bu', legend= stock+' Real Upper Band$', line_width = 2, color ='yellow', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bm', legend=stock + ' Real Middle Band', line_width=2, color='lightgreen', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bl', legend=stock + ' Real Lower Band', line_width=2, color='yellow', muted_color='grey', muted_alpha=0.2, source =source2)
    p2.legend.location = "top_left"
    p2.legend.click_policy = "mute"

    p3.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p3.line('x', 'z', legend=stock + ' price in $', line_width=2, color = 'blue', source = source3)
    p35.line('x2', 'rsi', legend= stock+' RSI', line_width = 2, color ='red', source = source3)
    rsi = gridplot([[p3], [p35]])

    p4.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p4.line('x', 'z', legend=stock + ' price in $', line_width=2, color ='blue', muted_color='grey', muted_alpha=0.2, source= source4)
    p45.line('x2','macd' ,legend=stock+' MACD', line_width=2, color='green', muted_color='grey', muted_alpha=0.2, source = source4)
    p45.line('x2', 'macds', color='orange', legend=stock+' MACD signal', line_width=2, muted_color='grey', muted_alpha=0.2, source= source4)
    p45.vbar(x=data4.index, bottom=[ 0 for _ in data4.index], top=data4['MACD_Hist'], width=4, color="purple", legend=stock+' MACD Histagram', line_width=2, muted_color='grey', muted_alpha=0.2)
    p45.legend.location = "top_left"
    p45.legend.click_policy = "mute"
    macd = gridplot([[p4], [p45]])

    p5.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p5.line('x','y',source=source5,legend= stock+' price in $', line_width = 2)
    p55.line(data.index, data['6. volume'], legend= stock+' Volume', line_width = 2, color ='purple')
    volume = gridplot([[p5], [p55]])

    prediction = pd.read_csv(os.path.join(os.path.dirname(__file__), "templates/predictx/symbols/"+stock+".csv"))
    days = 0,1 ,2,3,4,5,6,7,8,9,10,11,12,13,14,15
    pp1 = prediction.iloc[0]['pp']
    pp2 = prediction.iloc[1]['pp']
    pp3 = prediction.iloc[2]['pp']
    pp4 = prediction.iloc[3]['pp']
    pp5 = prediction.iloc[4]['pp']
    pp6 = prediction.iloc[5]['pp']
    pp7 = prediction.iloc[6]['pp']
    pp8 = prediction.iloc[7]['pp']
    pp9 = prediction.iloc[8]['pp']
    pp10 = prediction.iloc[9]['pp']
    pp11 = prediction.iloc[10]['pp']
    pp12 = prediction.iloc[11]['pp']
    pp13 = prediction.iloc[12]['pp']
    pp14 = prediction.iloc[13]['pp']
    pp15 = prediction.iloc[14]['pp']
    pp16 = prediction.iloc[15]['pp']
    p6.line(days,prediction['pp'], legend= stock+' Predicted price in $', line_width = 2)

    #Store components
    script, div = components(p)
    script1, div1 = components(p1)
    script2, div2 = components(p2)
    script3, div3 = components(rsi)
    script4, div4 = components(macd)
    script5, div5 = components(volume)
    script6, div6 = components(p6)

    #Feed them to the Django template.
    return render_to_response( 'predictx/symbol.html',
            {'script' : script , 'div' : div,'script1':script1, 'div1':div1,'script2' : script2 , 'div2' : div2,'script3' : script3 , 'div3' : div3,'script4' : script4 , 'div4' : div4,'script5' : script5 , 'div5' : div5
             ,'script6' : script6 , 'div6' : div6, 'wiki': wikiD,'sname':sname, "stocks":Stock.objects.all,'pp1':pp1,'pp2':pp2,'pp3':pp3,'pp4':pp4,'pp5':pp5,'pp6':pp6,'pp7':pp7,'pp8':pp8,'pp9':pp9,'pp10':pp10,'pp11':pp11,'pp12':pp12,'pp13':pp13,'pp14':pp14,'pp15':pp15,'pp16':pp16,
             'lHigh': lHigh,'lLow': lLow,'lClose': lClose,'lAdjClose': lAdjClose,'lVol': lVol,'lDiv': lDiv,'lSplit': lSplit,'lOpen': lOpen })

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
                return redirect('/AMZN')     #/dashboad
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
