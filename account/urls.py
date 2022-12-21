from django.urls import path
from . import views

urlpatterns = [
    path('account', views.wallet, name="wallet"),
    path('account/<int:pk>/addcash', views.add_cash, name="addcash"),
]
