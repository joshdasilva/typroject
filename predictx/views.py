from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from alpha_vantage.timeseries import TimeSeries


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
def MSFT(request):
    return render(request = request,
                  template_name='predictx/symbols/MSFT.html',
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
