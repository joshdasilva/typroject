from django.urls import path
from django.conf.urls import url
from . import views

app_name = "predictx"

urlpatterns = [
  #  path('', views.index),
    path("", views.indexpage, name="indexpage"),
    path("userguide/", views.userguide, name="userguide"),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),

    path("AAPL/", views.AAPL, name="AAPL"),
    path("MSFT/", views.MSFT, name="MSFT"),
    path("AMZN/", views.AMZN, name="AMZN"),
    path("FB/", views.FB, name="FB"),     #prediction
    path("BRK.B/", views.BRKB, name="BRK.B"),
    path("GOOG/", views.GOOG, name="GOOG"),  #prediction
    path("XOM/", views.XOM, name="XOM"),
    path("JPM/", views.JPM, name="JPM"),
    path("V/", views.V, name="V"),
    path("BAC/", views.BAC, name="BAC"),
    path("INTC/", views.INTC, name="INTC"),
    path("CSCO/", views.CSCO, name="CSCO"),
    path("VZ/", views.VZ, name="VZ"),
    path("PFE/", views.PFE, name="PFE"),
    path("T/", views.T, name="T"),
    path("MA/", views.MA, name="MA"),
    path("BA/", views.BA, name="BA"),
    path("DIS/", views.DIS, name="DIS"),
    path("KO/", views.KO, name="KO"),
    path("PEP/", views.PEP, name="PEP"),
    path("NFLX/", views.NFLX, name="NFLX"),
    path("MCD/", views.MCD, name="MCD"),
    path("WMT/", views.WMT, name="WMT"),
    path("ORCL/", views.ORCL, name="ORCL"),
    path("IBM/", views.IBM, name="IBM"),
    path("PYPL/", views.PYPL, name="PYPL"), #predi
    path("MMM/", views.MMM, name="MMM"),
    path("NVDA/", views.NVDA, name="NVDA"),
    path("NKE/", views.NKE, name="NKE"),
    path("COST/", views.COST, name="COST"),
    path("QCOM/", views.QCOM, name="QCOM"),

    path("AAPL/logout", views.logout_request, name="logout"),
    path("MSFT/logout", views.logout_request, name="logout"),
    path("AMZN/logout", views.logout_request, name="logout"),
    path("FB/logout", views.logout_request, name="logout"),
    path("BRK.B/logout", views.logout_request, name="logout"),
    path("GOOG/logout", views.logout_request, name="logout"),
    path("XOM/logout", views.logout_request, name="logout"),
    path("JPM/logout", views.logout_request, name="logout"),
    path("V/logout", views.logout_request, name="logout"),
    path("BAC/logout", views.logout_request, name="logout"),
    path("INTC/logout", views.logout_request, name="logout"),
    path("CSCO/logout", views.logout_request, name="logout"),
    path("VZ/logout", views.logout_request, name="logout"),
    path("PFE/logout", views.logout_request, name="logout"),
    path("T/logout", views.logout_request, name="logout"),
    path("MA/logout", views.logout_request, name="logout"),
    path("DIS/logout", views.logout_request, name="logout"),
    path("KO/logout", views.logout_request, name="logout"),
    path("PEP/logout", views.logout_request, name="logout"),
    path("NFLX/logout", views.logout_request, name="logout"),
    path("MCD/logout", views.logout_request, name="logout"),
    path("WMT/logout", views.logout_request, name="logout"),
    path("ORCL/logout", views.logout_request, name="logout"),
    path("IBM/logout", views.logout_request, name="logout"),
    path("PYPL/logout", views.logout_request, name="logout"),
    path("NVDA/logout", views.logout_request, name="logout"),
    path("NKE/logout", views.logout_request, name="logout"),
    path("COST/logout", views.logout_request, name="logout"),
    path("QCOM/logout", views.logout_request, name="logout"),

]

