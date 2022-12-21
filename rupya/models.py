from django.db import models
from django.conf import settings

class Wallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def tag(self):
        return self.owner.username

    def __str__(self) -> str:
        return self.owner.username
    
    
class Entrie(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='entries')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
        
class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='+')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20)
    transacted_at = models.DateTimeField(auto_now_add=True)