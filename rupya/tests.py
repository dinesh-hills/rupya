from django.test import TestCase
from .models import Transaction


class QuickTests(TestCase):

    def test_simple_test(self):

        lst = [Transaction()*2]

        print(lst)