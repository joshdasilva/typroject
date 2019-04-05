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


def chart(request):

    API_KEY = '90L3VT3DI22ZCS83'
    ts = TimeSeries(key='API_KEY', output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol='MSFT', outputsize='500')

    ti = TechIndicators(key='API_KEY', output_format='pandas')
    data2, meta_data2 = ti.get_bbands(symbol='MSFT', interval='daily', time_period=10)

    y= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415]
    title = 'Latest prices for Microsoft Inc.'

    data.index = pd.to_datetime(data.index)
    data2.index = pd.to_datetime(data2.index)
    pprint(data2)

    plot = figure(title= title ,
        x_axis_label= 'Date Time',
        x_axis_type="datetime",
        y_axis_label= 'Price in $',
        plot_width =800,
        plot_height =600)

    plot2 = figure(title=title,
                   x_axis_label='Date Time',
                   x_axis_type="datetime",
                   y_axis_label='Price in $',
                   plot_width=800,
                   plot_height=600)
    plot.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    plot.line(data.index, data['4. close'], legend= 'MSFT in $', line_width = 2)

    plot2.xaxis.formatter = DatetimeTickFormatter(days="%Y-%m-%d")
    plot2.line(data2.index, data2['Real Middle Band'], legend= 'MSFT Middle band $', line_width = 2)

    #Store components
    script, div = components(plot)
    script2, div2 = components(plot2)

    #Feed them to the Django template.
    return render_to_response( 'predictx/symbols/MSFT.html',
            {'script' : script , 'div' : div,'script2' : script2 , 'div2' : div2})


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


def MSFT(request):
    return render(request = request,
                  template_name='predictx/symbols/MSFT.html',
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

