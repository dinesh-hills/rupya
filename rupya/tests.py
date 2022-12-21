from django.test import TestCase
from .models import Wallet
# Create your tests here.

wallet = Wallet.objects.get(owner_id=3)
print(wallet)