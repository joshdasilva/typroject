from django.urls import path
from . import views

app_name = "predictx"

urlpatterns = [
  #  path('', views.index),
    path("", views.indexpage, name="indexpage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login"),
    path("dashboard/logout", views.logout_request, name="logout"),
]

