from pprint import pprint
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from core.models import User
from rupya.models import Wallet

@pytest.mark.django_db
class TestUserTransactions:

    def test_if_not_a_user_return_404(self):
        client = APIClient()
        user_id = -1
        response = client.get(f'/wallet/{user_id}')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_new_user_has_wallet_return_200(self):
        user = baker.make(User)
        client = APIClient()
        response = client.get(f'/wallet/{user.id}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['balance'] == 0

    def test_if_user_deposit_increase_user_and_internal_balance(self):
        user = baker.make(User)
        client = APIClient()
        
        response = client.post(f'/wallet/{user.id}/deposit', data={
            "from_wallet": user.id,
            "to_wallet": 2,
            "amount": 100
        })

        pprint(response)

        assert False