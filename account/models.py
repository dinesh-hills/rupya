from django.db import models
from django.conf import settings

class Wallet(models.Model):
    balance = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def tag(self):
        return self.user.username

    def __str__(self) -> str:
        return f'₹{self.user}'