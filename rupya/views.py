from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, Wallet
from .serializers import SendReceiveSerializer, TransactionSerializer, DepositWithdrawSerializer, WalletSerializer


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

class DepositWithdrawView(APIView):
    def get(self, request, pk):
        wallet = Wallet.objects.get(pk=pk)
        seriazlier = WalletSerializer(wallet)
        return Response(seriazlier.data)
    
    def post(self, request, pk):
        serializer = DepositWithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.path.endswith('deposit'):
            serializer.context['transaction_type'] = 'Deposit'
        elif request.path.endswith('withdraw'):
            serializer.context['transaction_type'] = 'Withdraw'

        wallet = serializer.save()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
        
        
class TransactionListView(APIView):
    def get(self, request, pk):
        queryset = Transaction.objects.filter(Q(from_wallet=pk) | Q(to_wallet=pk)).all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
        
        
class SendReceviceView(APIView):
    # Browsable API view.
    name = ''
    
    def get(self, request, pk):
        # Browsable API view.
        if request.path.endswith('send'):
            self.name = 'Send Cash'
        
        wallet = Wallet.objects.get(pk=pk)
        seriazlier = WalletSerializer(wallet)
        return Response(seriazlier.data)
    
    def post(self, request, pk):
        serializer = SendReceiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.path.endswith('send'):
            serializer.context['sender_wallet_id'] = pk
            serializer.context['transaction_type'] = 'Send'

        wallet = serializer.save()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)