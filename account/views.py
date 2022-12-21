from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wallet
from .serializers import AddCashSerializer, WalletSerializer


@api_view()
def wallet(request):
    queryset = Wallet.objects.all()
    seriazlier = WalletSerializer(data=queryset, many=True)
    seriazlier.is_valid()
    return Response(seriazlier.data)


@api_view(['GET', 'POST'])
def add_cash(request, pk):
    user = Wallet.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = WalletSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AddCashSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response("Ok")