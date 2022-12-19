from rest_framework import serializers


class walletSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tag = serializers.CharField(max_length=25)
    balance = serializers.IntegerField()
    user = serializers.IntegerField()