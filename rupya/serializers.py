from rest_framework import serializers

from .models import CashRequest, Transaction, Wallet
from .const import TRANSACTION_TYPE_DEPOSIT, TRANSACTION_TYPE_WITHDRAW


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
        
        if self.context['transaction_type'] == 'Send':
            sender_wallet_id = self.context['sender_wallet_id']

            Transaction.objects.create(
                transaction_type='send',
                **self.validated_data
            )

            ###########
            # Add a transaction record as received for the receiver wallet.
            ###########
            
            sender_wallet = Wallet.objects.get(pk=sender_wallet_id)
            receiver_wallet = Wallet.objects.get(pk=self.validated_data['to_wallet'].id)
            
            sender_wallet.balance -= self.validated_data['amount']
            receiver_wallet.balance += self.validated_data['amount']
        
            sender_wallet.save()
            receiver_wallet.save()
            
            self.instance = sender_wallet
            return self.instance
        
        # Request received to the sender.
        if self.context['transaction_type'] == 'Request':
            sender_wallet_id = self.context['sender_wallet_id']
            pass
        
        
        
    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_wallet', 'amount']
    

class CashRequestSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    
    class Meta:
        model = CashRequest
        fields = ['id', 'request_id', 'from_wallet', 'to_wallet', 'amount']
        read_only_field = ['request_id']