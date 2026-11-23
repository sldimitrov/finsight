from django.test import TestCase

from .forms import AccountForm
from .models import Account
from users.models import User
from transactions.models import Transaction
from django.db.models import ProtectedError



class AccountFormTests(TestCase):
    def test_valid_account_data_is_accepted(self):
        form = AccountForm(
            data={
                "name": "Everyday account",
                "type": "checking",
                "balance": "125.50",
                "currency": "BGN",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_account_type_is_rejected(self):
        form = AccountForm(
            data={
                "name": "Everyday account",
                "type": "unknown",
                "balance": "125.50",
                "currency": "BGN",
            }
        )

        self.assertFalse(form.is_valid())

    def test_user_and_active_status_are_not_editable(self):
        form = AccountForm()

        self.assertNotIn("user", form.fields)
        self.assertNotIn("is_active", form.fields)

    def test_account_with_transactions_cannot_be_deleted(self):
        # Create an account and a transaction associated with it
        user = User.objects.create_user(
            username="testuser", password="testpass", email="test@example.com", first_name="Test", last_name="User"
        )
        account = Account.objects.create(
            user=user, name="Test Account", type="checking", balance=100.00, currency="USD"
        )
        Transaction.objects.create(
            account=account,
            date="2023-01-01",
            type="income",
            amount=50.00,
            description="Test transaction",
            category="Test category",
        )

        with self.assertRaises(ProtectedError):
            account.delete()