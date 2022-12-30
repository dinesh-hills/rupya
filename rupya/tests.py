from django.test import TestCase
from .models import Transaction

transaction = Transaction.objects.all()
transaction.delete()

