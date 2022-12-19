from django.urls import path
from . import views

urlpatterns = [
    path('account', views.wallet, name="wallet"),
]
