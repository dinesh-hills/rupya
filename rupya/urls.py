from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.WalletListView.as_view(), name="wallet"),
    path('user/<int:pk>', views.WalletDetailView.as_view(), name="wallet-detail"),
    path('user/transactions', views.TransactionListView.as_view(), name="transactions-list"),
    path('user/<int:pk>/transactions', views.TransactionDetailView.as_view(), name="transactions-detail"),
    
    path('user/<int:pk>/deposit', views.DepositWithdrawView.as_view(), name="deposit"),
    path('user/<int:pk>/withdraw', views.DepositWithdrawView.as_view(), name="withdraw"),
    
    path('user/<int:pk>/send', views.SendReceviceView.as_view(), name="send"),
    path('user/<int:pk>/receive', views.SendReceviceView.as_view(), name="receive"),
    path('user/<int:pk>/requests', views.CashRequestListView.as_view(), name="requests"),
    path('user/<int:pk>/requests/<int:req_pk>', views.CashRequestDetailView.as_view(), name="requests-detail"),
]