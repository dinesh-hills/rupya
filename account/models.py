from django.db import models
from django.conf import settings

class wallet:
    tag = models.CharField(max_length=25, unique=True)
    balance = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)