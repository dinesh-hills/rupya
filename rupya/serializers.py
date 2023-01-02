from random import getrandbits
from rest_framework import serializers
from .models import CashRequest, Transaction, Wallet
from .const import TRANSACTION_TYPE_DEPOSIT, TRANSACTION_TYPE_RECEIVE, TRANSACTION_TYPE_SEND, TRANSACTION_TYPE_WITHDRAW


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owner_id', 'tag', 'balance']
        

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'from_wallet', 'to_wallet', 'amount', 'transaction_type', 'transacted_at']


        

class DepositWithdrawSerializer(serializers.ModelSerializer):

    @staticmethod
    def create_transactions(transaction_type ,depositer_wallet_id, amount) -> Wallet:
        # A default acc
        internal_acc_id = 3

        internal_acc = Wallet.objects.get(owner_id=internal_acc_id)
        user_wallet = Wallet.objects.get(pk=depositer_wallet_id)
        transact = Transaction()

        if transaction_type == TRANSACTION_TYPE_DEPOSIT:
            internal_acc.balance += amount
            user_wallet.balance += amount
            transact.amount = amount
            transact.from_wallet = internal_acc
            transact.to_wallet = user_wallet
            transact.transaction_type = transaction_type

        elif transaction_type == TRANSACTION_TYPE_WITHDRAW:
            internal_acc.balance -= amount
            user_wallet.balance -= amount
            transact.amount = amount
            transact.from_wallet = user_wallet
            transact.to_wallet = internal_acc
            transact.transaction_type = transaction_type

        transact.save()
        internal_acc.save()
        user_wallet.save()
        
        return user_wallet
    
    def save(self, **kwargs):
        self.instance = self.create_transactions(self.context['transaction_type'], self.context['user_wallet_id'] ,self.validated_data['amount'])
        return self.instance
    

    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_wallet', 'amount']
        read_only_fields = ['from_wallet', 'to_wallet']


class SendReceiveSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        
        if self.context['transaction_type'] == TRANSACTION_TYPE_SEND:
            sender_wallet_id = self.context['sender_wallet_id']
            receiver_wallet = self.validated_data['to_wallet']
            amount = self.validated_data['amount']

            sender_wallet = Wallet.objects.get(pk=sender_wallet_id)
            
            sender_wallet.balance -= amount
            receiver_wallet.balance += amount


            ttypes = [TRANSACTION_TYPE_SEND, TRANSACTION_TYPE_RECEIVE]

            transactions = []
            for ttype in ttypes:
                t = Transaction()
                t.from_wallet = sender_wallet
                t.to_wallet = receiver_wallet
                t.amount = amount
                t.transaction_type = ttype
                transactions.append(t)

            Transaction.objects.bulk_create(transactions)

            sender_wallet.save()
            receiver_wallet.save()
            
            self.instance = sender_wallet
            return self.instance
        
        
    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_wallet', 'amount']
        read_only_fields = ['from_wallet']


class CashRequestSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        requester_wallet = Wallet.objects.get(pk=self.context['requester_wallet_id'])
        recipient_wallet = self.validated_data['from_wallet']
        amount = self.validated_data['amount']

        cash_request = CashRequest()
        cash_request.request_id = getrandbits(32)
        cash_request.from_wallet = recipient_wallet
        cash_request.to_wallet = requester_wallet
        cash_request.amount = amount
        cash_request.save()

        self.instance = cash_request
        return self.instance


    class Meta:
        model = CashRequest
        fields = ['id', 'request_id', 'from_wallet', 'to_wallet', 'amount', 'req_status', 'created_at']
        read_only_fields = ['id', 'request_id', 'to_wallet', 'req_status', 'created_at']