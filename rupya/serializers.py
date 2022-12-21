from rest_framework import serializers
from .models import Entrie, Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owner_id', 'tag', 'balance']
        
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'from_wallet', 'to_wallet', 'amount', 'transaction_type', 'transacted_at']
        

class WalletDepositSerializer(serializers.ModelSerializer):
    
    def save(self, **kwargs):
        Transaction.objects.create(**self.validated_data)
        
        Entrie.objects.create(
            wallet=self.validated_data['to_wallet'],
            amount=self.validated_data['amount']
        )
        
        deposit = Wallet.objects.get(owner_id=3)
        deposit.balance += self.validated_data['amount']
        deposit.save()
        
        wallet = Wallet.objects.get(pk=self.validated_data['to_wallet'].id)
        wallet.balance += self.validated_data['amount']
        wallet.save()
        
        self.instance = wallet
        
        return self.instance
    
    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_wallet', 'amount', 'transaction_type']
    


# class AddCashSerializer(serializers.Serializer):
#     amount = serializers.IntegerField(source='balance')
    
#     def create(self, validated_data):
#         wallet = Wallet.objects.get(user_id=self.context['wallet_id'])
#         wallet.balance += validated_data['balance']
#         wallet.save()
#         self.instance = wallet
#         return self.instance
    
# class DepositSerializer(serializers.Serializer):
#     amount = serializers.IntegerField(source='balance')
    
#     def create(self, validated_data):
#         wallet = Wallet.objects.get(user_id=self.context['wallet_id'])
#         wallet.balance -= validated_data['balance']
#         wallet.save()
#         self.instance = wallet
#         return self.instance
    
# class TransferSerializer(serializers.Serializer):
#     to_wallet = serializers.IntegerField()
#     amount = serializers.IntegerField()
    
#     def create(self, validated_data):
#         from_wallet_id = self.context['from_wallet']
#         to_wallet_id = validated_data['to_wallet']
#         amount = validated_data['amount']
        
#         from_wallet = Wallet.objects.get(pk=from_wallet_id)
#         to_wallet = Wallet.objects.get(pk=to_wallet_id)
        
#         from_wallet.balance -= amount
#         to_wallet.balance += amount
        
#         Transfer.objects.create(
#             to_wallet=to_wallet,
#             amount=amount,
#             transaction_type='tranfer'
#         )
        
#         from_wallet.save()
#         to_wallet.save()
        
#         self.instance = from_wallet
        
#         return self.instance

    
# class TransactionHistory(serializers.Serializer):
#     to_wallet = serializers.PrimaryKeyRelatedField(read_only=True)
#     amount = serializers.IntegerField()
#     transaction_type = serializers.CharField()
#     transacted_at = serializers.DateTimeField()