from django.db import models
from django.conf import settings
from .const import CASHREQUEST_STATUS_CHOICES, CASHREQUEST_STATUS_PENDING

class Wallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def tag(self):
        return self.owner.username

    def __str__(self) -> str:
        return self.owner.username
    
        
class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20)
    transacted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Transaction {self.from_wallet.owner}'
    
    
    
class CashRequest(models.Model):
    request_id = models.BigIntegerField()
    from_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    amount = models.IntegerField()
    req_status = models.CharField(max_length=1, choices=CASHREQUEST_STATUS_CHOICES, default=CASHREQUEST_STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
