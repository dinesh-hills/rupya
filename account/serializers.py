from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tag = serializers.CharField(max_length=25)
    balance = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
    
class AddCashSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    
    def create(self, validated_data):
        user = Wallet.objects.get(pk=validated_data['user_id'])
        user.balance += validated_data['amount']
        user.save()

        return self.instance