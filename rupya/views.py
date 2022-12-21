from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletDepositSerializer, WalletSerializer


class WalletListView(APIView):
    def get(self, request):
        queryset = Wallet.objects.all()
        seriazlier = WalletSerializer(queryset, many=True)
        return Response(seriazlier.data)
        
class WalletDetailView(APIView):
    def get(self, request, pk):
        wallet = Wallet.objects.get(pk=pk)
        seriazlier = WalletSerializer(wallet)
        return Response(seriazlier.data)

class WalletDepositView(APIView):
    def get(self, request, pk):
        wallet = Wallet.objects.get(pk=pk)
        seriazlier = WalletSerializer(wallet)
        return Response(seriazlier.data)
    
    def post(self, request, pk):
        serializer = WalletDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = serializer.save()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
        


# @api_view(['GET', 'POST'])
# def deposit(request, pk):
#     user = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = WalletSerializer(user)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = AddCashSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.context['wallet_id'] = pk
#         wallet = serializer.save()
#         serializer = WalletSerializer(wallet)
#         return Response(serializer.data)
    

# @api_view(['GET', 'POST'])
# def withdraw(request, pk):
#     user = Wallet.objects.get(pk=pk)
#     if request.method == 'GET':
#         serializer = WalletSerializer(user)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = DepositSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.context['wallet_id'] = pk
#         wallet = serializer.save()
#         serializer = WalletSerializer(wallet)
#         return Response(serializer.data)
    
# @api_view(['GET', 'POST'])
# def transfer(request, pk):
#     if request.method == 'GET':
#         from_wallet = Wallet.objects.get(pk=pk)
#         serializer = WalletSerializer(from_wallet)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = TransferSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.context['from_wallet'] = pk
#         sender_wallet = serializer.save()
#         serializer = WalletSerializer(sender_wallet)
#         return Response(serializer.data)
    
    
# @api_view()
# def transaction_history(request, pk):
#     queryset = Transaction.objects.filter(Q(from_wallet_id=pk) | Q(to_wallet_id=pk)).all()
#     serializer = TransactionHistory(queryset, many=True)
#     return Response(serializer.data)