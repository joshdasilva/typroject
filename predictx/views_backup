from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import NewUserForm
from math import pi
from bokeh.layouts import row, column, gridplot
from bokeh.plotting import figure, output_file, show, curdoc, _figure
from bokeh.embed import components
from bokeh.driving import count
from bokeh.models import DatetimeTickFormatter,HoverTool, ColumnDataSource, Slider, Select, BasicTickFormatter
from pprint import pprint
import pandas as pd
import wikipedia, os
from alphaVantageAPI.alphavantage import AlphaVantage
from stockstats import StockDataFrame

key = "U5HDNUUWSMV4P355"

AV = AlphaVantage(api_key=key,premium=True,output_size='Full',datatype='json',export=False,export_path='~/av_data',output='csv',clean=False,proxy={})

def chart(stock, sname, wikiD):
    #set title for all graphs
    title = 'Latest prices for'+sname

    data = AV.data(function='DA', symbol=stock)
    #intd= AV.intraday(symbol=stock, stock=60)
    data2 = AV.data(symbol=stock, interval='daily', function='BBANDS', series_type='close', time_period=20)
    data3 = AV.data(symbol=stock, interval='daily', function='RSI', series_type='close', time_period=20)
    data4 = AV.data(symbol=stock, interval='daily', function='MACD', series_type='close', time_period=20)

    #reshaping the arrays to a fixed length
    s = 5321
    data = data.tail(s)
    data2 = data2.tail(s)
    data3 = data3.tail(s)
    data4 = data4.tail(s)

    #candle stick data
    cdata = data.tail(331)

    #processing date time for candlesticks and regular data
    cdataindex = cdata['date']
    dataindex = data['date']
    cdataindex = pd.to_datetime(cdataindex)
    dataindex = pd.to_datetime(dataindex)

    #processed data
    adjClose = data['5. adjusted close']
    close = data['4. close']

    #calculations for 200 day EMA/SMA and 20 day EMA/SMA
    long_rolling = adjClose.rolling(window=200).mean()
    short_rolling = adjClose.rolling(window=20).mean()
    ema_short = adjClose.ewm(span=20, adjust=False).mean()
    ema_long = adjClose.ewm(span=200, adjust=False).mean()

    # #bollinger bands calculation
    # data2['Real Middle Band'] = data['5. adjusted close'].rolling(window=20).mean()
    # stddev = data['5. adjusted close'].rolling(window=20).std()
    # data2['Real Upper Band'] = data2['Real Middle Band'] + (stddev*2)
    # data2['Real Lower Band'] = data2['Real Middle Band'] - (stddev*2)

    #calculation for RSI inspired from Stackoverflow user's Moots answer availble at :https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
    # length = 20
    # delta = adjClose.diff()
    # delta = delta[1:]
    # up, down = delta.copy(), delta.copy()
    # up[up < 0.0] = 0.0
    # down[down > 0.0] = 0.0
    #
    # # Calculate the EWMA
    # roll_up1 = up.ewm(com=(length - 1), min_periods=length).mean()
    # roll_down1 = down.abs().ewm(com=(length - 1), min_periods=length).mean()
    #
    # #Calculate the RSI based on EWMA
    # RS1 = roll_up1 / roll_down1
    # RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    #calculation for MACD
    # emaa = StockDataFrame.retype(adjClose)
    # emaa['macd'] = emaa.get('macd')  # calculate MACD
    # emaa['ema12'] = adjClose.ewm(span=12, adjust=False).mean
    # emaa['ema26'] = adjClose.ewm(span=26, adjust=False).mean

    #Latest data
    latest = data.tail(1)
    lOpen = latest.iloc[:, 1:2].values
    lOpen=str(lOpen).lstrip('[').rstrip(']')
    lHigh = latest.iloc[:, 2:3].values
    lHigh=str(lHigh).lstrip('[').rstrip(']')
    lLow = latest.iloc[:, 3:4].values
    lLow=str(lLow).lstrip('[').rstrip(']')
    lClose = latest.iloc[:, 4:5].values
    lClose=str(lClose).lstrip('[').rstrip(']')
    lAdjClose = latest.iloc[:, 5:6].values
    lAdjClose=str(lAdjClose).lstrip('[').rstrip(']')
    lVol = latest.iloc[:, 6:7].values
    lVol=str(lVol).lstrip('[').rstrip(']')
    lDiv = latest.iloc[:, 7:8].values
    lDiv=str(lDiv).lstrip('[').rstrip(']')
    lSplit = latest.iloc[:, 8:9].values
    lSplit=str(lSplit).lstrip('[').rstrip(']')

    source0 = ColumnDataSource(data=dict(x=cdataindex, y=cdata['5. adjusted close'], o=cdata['1. open'], h=cdata['2. high'], l=cdata['3. low'],c=cdata['4. close'], vol=cdata['6. volume']))
    source1 = ColumnDataSource(data=dict(x=dataindex, y=adjClose, ssma=short_rolling, lsma=long_rolling, sema=ema_short,lema=ema_long))
    source2 = ColumnDataSource(data=dict(x = dataindex, z= close , bu=data2['Real Upper Band'], bm=data2['Real Middle Band'], bl=data2['Real Lower Band']))
    source3 = ColumnDataSource(data=dict(x = dataindex, z=close, rsi = data3['RSI']))
    source4 = ColumnDataSource(data=dict(x = dataindex, z=close, macd=data4['MACD'], macds = data4['MACD_Signal']))
    source5 = ColumnDataSource(data=dict(x = dataindex, y=adjClose,o=data['1. open'],h=data['2. high'],l=data['3. low'],c=close, vol=data['6. volume']))

    p = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =1300,
        plot_height =600,
        tools=['pan', 'wheel_zoom', 'box_zoom', 'reset'])
    p.add_tools(HoverTool(tooltips=[("(Date","@x{%F}"), ("Adjusted Close", "@y{%0.2f}"), ("open", "@o{%0.2f}"), ("high", "@h{%0.2f}"), ("low", "@l{%0.2f}"), ("close", "@c{%0.2f}"), ("Volume", "@vol{%0.2f}")],
        formatters={
            'x': 'datetime',
            'y': 'printf',
            'o': 'printf',
            'h': 'printf',
            'l': 'printf',
            'c': 'printf',
            'vol':'printf'
        },
        mode='vline')
    )

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
        mode='mouse'))

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
        mode='mouse'))
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
    p5.add_tools(HoverTool(tooltips=[("(Date","@x{%F}"), ("Adjusted Close", "@y{%0.2f}"), ("open", "@o{%0.2f}"), ("high", "@h{%0.2f}"), ("low", "@l{%0.2f}"), ("close", "@c{%0.2f}"), ("Volume", "@vol{%0.2f}")],
        formatters={
            'x': 'datetime',
            'y': 'printf',
            'o': 'printf',
            'h': 'printf',
            'l': 'printf',
            'c': 'printf',
            'vol':'printf'

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



    inc = cdata['4. close'] > cdata['1. open']
    dec = cdata['1. open'] > cdata['4. close']
    w = 12 * 60 * 60 * 1000  # half day in ms
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    p.segment(cdataindex, cdata['2. high'], cdataindex, cdata['3. low'], color="black")
    p.vbar(cdataindex[inc], w, cdata['1. open'][inc], cdata['4. close'][inc], fill_color="#7cfc00", line_color="black")
    p.vbar(cdataindex[dec], w, cdata['1. open'][dec], cdata['4. close'][dec], fill_color="#ff0000", line_color="black")
    p.line('x', 'y', line_width=2,legend= stock, color='lightgrey', muted_color='grey', muted_alpha=0.2,
            source=source0)
    p.legend.location = "top_left"
    p.legend.click_policy = "mute"


    p1.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p1.line('x','y', legend= stock+' price in $', line_width = 2,color='blue', muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'lsma', legend= stock+' 200 day MA', line_width = 2, color ='red',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'ssma', legend= stock+' 20 day MA', line_width = 2, color ='yellow',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'lema', legend= stock+' 200 day EMA', line_width = 2, color ='green',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.line('x', 'sema', legend= stock+' 20 day EMA', line_width = 2, color ='orange',  muted_color='grey', muted_alpha=0.2, source=source1)
    p1.legend.location = "top_left"
    p1.legend.click_policy = "mute"

    p2.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p2.line('x', 'z', legend= stock+' price in $', line_width = 2, color ='blue', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bu', legend= stock+' Real Upper Band$', line_width = 2, color ='yellow', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bm', legend=stock + ' Real Middle Band', line_width=2, color='lightgreen', muted_color='grey', muted_alpha=0.2, source=source2)
    p2.line('x', 'bl', legend=stock + ' Real Lower Band', line_width=2, color='orange', muted_color='grey', muted_alpha=0.2, source =source2)
    p2.legend.location = "top_left"
    p2.legend.click_policy = "mute"

    p3.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p3.line('x', 'z', legend=stock + ' price in $', line_width=2, color = 'blue', source = source3)
    p35.line('x', 'rsi', legend= stock+' RSI', line_width = 2, color ='red', source = source3) #x2
    rsi = gridplot([[p3], [p35]])

    p4.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p4.line('x', 'z', legend=stock + ' price in $', line_width=2, color ='blue', muted_color='grey', muted_alpha=0.2, source= source4)
    p45.line('x','macd' ,legend=stock+' MACD', line_width=2, color='orange', muted_color='grey', muted_alpha=0.2, source = source4) #x2
    p45.line('x', 'macds', color='green', legend=stock+' MACD signal', line_width=2, muted_color='grey', muted_alpha=0.2, source= source4) #x2
    p45.vbar(x=dataindex, bottom=[ 0 for _ in dataindex], top=data4['MACD_Hist'], width=4, color="purple", legend=stock+' MACD Histagram', line_width=2, muted_color='grey', muted_alpha=0.2)#data4.index
    p45.legend.location = "top_left"
    p45.legend.click_policy = "mute"
    macd = gridplot([[p4], [p45]])

    p5.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    p5.line('x','y',legend= stock+' price in $', line_width = 2,source=source5)
    p55.line('x', 'vol', legend= stock+' Volume', line_width = 2, color ='purple', source=source5)
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


def indexpage(request):
    return render(request, 'predictx/index.html')

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

def userguide(request):
    return render(request, 'predictx/userguide.html')


# def favorite_stock(request, id):
#     stock = get_object_or_404(Stock,id=id)
#     if stock.favorite.filter(id=request.user.id).exists():
#         stock.favorite.remove(request.user)
#     else:
#         stock.favorite.add(request.user)
#     return HttpResponseRedirect(stock.get_absolute_url())
#
# def stock_favorite_list(request):
#     user = request.user
#     favorite_stocks = user.favorite.all()
#     context = {
#         'favorite_stocks': favorite_stocks
#     }
#     return render(request, 'predictx/symbol.html', context)
#
# def stock_detail(request, id):
#     stock = get_object_or_404(Stock, id=id)
#     is_favourite=False
#     if stock.favorite.filter(id=request.user.id).exists():
#         is_favourite=True
#
#     context = {
#         ' is_favourite': is_favourite
#     }
#     return render(request, 'predictx/symbol.html', context)


def MSFT(request):
    if request.user.is_authenticated:
        stock = 'MSFT'
        sname='Microsoft Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")


def AAPL(request):
    if request.user.is_authenticated:
        stock = 'AAPL'
        sname = 'Apple Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def AMZN(request):
    if request.user.is_authenticated:
        stock = 'AMZN'
        sname = 'Amazon.com Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def FB(request):
    if request.user.is_authenticated:
        stock = 'FB'
        sname = 'Facebook Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def BRKB(request):
    if request.user.is_authenticated:
        stock = 'BRK.B'
        sname = 'Berkshire Hathaway Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def GOOG(request):
    if request.user.is_authenticated:
        stock = 'GOOG'
        sname = 'Alphabet Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def XOM(request):
    if request.user.is_authenticated:
        stock = 'XOM'
        sname = 'Exxon Mobil Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def JPM(request):
    if request.user.is_authenticated:
        stock = 'JPM'
        sname = 'JPMorgan Chase & Co.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def V(request):
    if request.user.is_authenticated:
        stock = 'V'
        sname = 'Visa Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def BAC(request):
    if request.user.is_authenticated:
        stock = 'BAC'
        sname = 'Bank of America Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def INTC(request):
    if request.user.is_authenticated:
        stock = 'INTC'
        sname = 'Intel Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def CSCO(request):
    if request.user.is_authenticated:
        stock = 'CSCO'
        sname = 'Cisco Systems Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def VZ(request):
    if request.user.is_authenticated:
        stock = 'VZ'
        sname = 'Verizon Communications Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def PFE(request):
    if request.user.is_authenticated:
        stock = 'PFE'
        sname = 'Pfizer Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def T(request):
    if request.user.is_authenticated:
        stock = 'T'
        sname = 'AT&T Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def MA(request):
    if request.user.is_authenticated:
        stock = 'MA'
        sname = 'Mastercard Incorporated'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def BA(request):
    if request.user.is_authenticated:
        stock = 'BA'
        sname = 'Boeing Company'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def DIS(request):
    if request.user.is_authenticated:
        stock = 'DIS'
        sname = 'Walt Disney Company'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def KO(request):
    if request.user.is_authenticated:
        stock = 'KO'
        sname = 'Coca-Cola Company'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def PEP(request):
    if request.user.is_authenticated:
        stock = 'PEP'
        sname = 'PepsiCo Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def NFLX(request):
    if request.user.is_authenticated:
        stock = 'NFLX'
        sname = 'Netflix Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def MCD(request):
    if request.user.is_authenticated:
        stock = 'MCD'
        sname = 'McDonalds Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def WMT(request):
    if request.user.is_authenticated:
        stock = 'WMT'
        sname = 'Walmart Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def ORCL(request):
    if request.user.is_authenticated:
        stock = 'ORCL'
        sname = 'Oracle Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def IBM(request):
    if request.user.is_authenticated:
        stock = 'IBM'
        sname = 'IBM'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def PYPL(request):
    if request.user.is_authenticated:
        stock = 'PYPL'
        sname = 'Paypal'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def MMM(request):
    if request.user.is_authenticated:
        stock = 'MMM'
        sname = '3M Company'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def NVDA(request):
    if request.user.is_authenticated:
        stock = 'NVDA'
        sname = 'Nvidia Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def NKE(request):
    if request.user.is_authenticated:
        stock = 'NKE'
        sname = 'Nike Inc.'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def COST(request):
    if request.user.is_authenticated:
        stock = 'COST'
        sname = 'Costco Wholesale Corporation'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")

def QCOM(request):
    if request.user.is_authenticated:
        stock = 'QCOM'
        sname = 'Qualcomm Incorporated'
        wikiD = wikipedia.summary(sname, sentences=5)
        return chart(stock, sname, wikiD)
    else:
        return redirect("predictx:login")
