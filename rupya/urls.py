from django.urls import path
from . import views

urlpatterns = [
    path('', views.WalletListView.as_view(), name="wallet"),
    path('<int:pk>', views.WalletDetailView.as_view(), name="wallet-detail"),
    path('<int:pk>/deposit', views.WalletDepositView.as_view(), name="deposit"),
    # path('<int:pk>/deposit', views.withdraw, name="deposit"),
    # path('<int:pk>/transfer', views.transfer, name="send-cash"),
    # path('<int:pk>/transactions', views.transaction_history, name="transactions"),
]