from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.WalletListView.as_view(), name="wallet"),
    path('<int:pk>', views.WalletDetailView.as_view(), name="wallet-detail"),
    path('<int:pk>/transactions', views.TransactionDetailView.as_view(), name="transactions"),
    
    path('<int:pk>/deposit', views.DepositWithdrawView.as_view(), name="deposit"),
    path('<int:pk>/withdraw', views.DepositWithdrawView.as_view(), name="withdraw"),
    
    path('<int:pk>/send', views.SendReceviceView.as_view(), name="send"),
]