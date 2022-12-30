from itertools import chain
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, Wallet
from .serializers import CashRequestSerializer, SendReceiveSerializer, TransactionSerializer, DepositWithdrawSerializer, WalletSerializer
from .const import TRANSACTION_TYPE_DEPOSIT, TRANSACTION_TYPE_RECEIVE, TRANSACTION_TYPE_REQUEST, TRANSACTION_TYPE_SEND, TRANSACTION_TYPE_WITHDRAW


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
        serializer.context['user_wallet_id'] = pk

        if request.path.endswith('deposit'):
            serializer.context['transaction_type'] = TRANSACTION_TYPE_DEPOSIT
        elif request.path.endswith('withdraw'):
            serializer.context['transaction_type'] = TRANSACTION_TYPE_WITHDRAW

        wallet = serializer.save()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
        
        
class TransactionDetailView(APIView):
    def get(self, request, pk):
        send_withdraw_qs = Transaction.objects.filter(Q(transaction_type=TRANSACTION_TYPE_SEND) | Q(transaction_type=TRANSACTION_TYPE_WITHDRAW), from_wallet=pk)
        deposit_receive_qs = Transaction.objects.filter(Q(transaction_type=TRANSACTION_TYPE_DEPOSIT) | Q(transaction_type=TRANSACTION_TYPE_RECEIVE), to_wallet=pk)
        queryset = chain(send_withdraw_qs, deposit_receive_qs)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
        


        
class SendReceviceView(APIView):
    # Browsable API view.
    name = ''

    def initial(self, request, *args, **kwargs):
        if request.path.endswith('send'):
            self.name = 'Send Cash'
        elif request.path.endswith('receive'):
            self.name = 'Receive Cash'

        return super().initial(request, *args, **kwargs)
        
    def post(self, request, pk):
        
        if request.path.endswith('send'):
            serializer = SendReceiveSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.context['sender_wallet_id'] = pk
            serializer.context['transaction_type'] = TRANSACTION_TYPE_SEND
            wallet = serializer.save()
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)

        elif request.path.endswith('receive'):
            serializer = CashRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.context['requester_wallet_id'] = pk
            serializer.context['transaction_type'] = TRANSACTION_TYPE_REQUEST
            request_obj = serializer.save()
            serializer = WalletSerializer(request_obj)
            return Response(serializer.data)
