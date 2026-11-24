from django.test import TestCase

from .forms import AccountForm
from .models import Account
from users.models import User
from django.urls import reverse
from transactions.models import Transaction
from django.db.models import ProtectedError



class AccountFormTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="test@example.com", first_name="Test", last_name="User"
        )

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
        account = Account.objects.create(
            user=self.user, name="Test Account", type="checking", balance=100.00, currency="USD"
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

    def test_can_not_view_someone_elses_account(self):
        user2 = User.objects.create_user(
            username="testuser2", password="testpass", email="test2@example.com", first_name="Test", last_name="User2"
        )
        account = Account.objects.create(
            user=self.user, name="Test Account", type="checking", balance=100.00, currency="USD"
        )

        self.client.force_login(user2)
        response = self.client.get(reverse("accounts:detail", args=[account.pk]))
        self.assertEqual(response.status_code, 404)

    def test_can_not_add_transaction_to_someone_elses_account(self):
        user2 = User.objects.create_user(
            username="testuser2", password="testpass", email="test2@example.com", first_name="Test", last_name="User2"
        )
        account = Account.objects.create(
            user=self.user, name="Test Account", type="checking", balance=100.00, currency="USD"
        )

        self.client.force_login(user2)
        response = self.client.get(reverse("accounts:create_transaction", args=[account.pk]))
        self.assertEqual(response.status_code, 404)

    def test_can_not_delete_someone_elses_transaction(self):
        user2 = User.objects.create_user(
            username="testuser2", password="testpass", email="test2@example.com", first_name="Test", last_name="User2"
        )
        account = Account.objects.create(
            user=self.user, name="Test Account", type="checking", balance=100.00, currency="USD"
        )
        transaction = Transaction.objects.create(
            account=account,
            date="2023-01-01",
            type="income",
            amount=50.00,
            description="Test transaction",
            category="Test category",
        )

        self.client.force_login(user2)
        response = self.client.get(reverse("transactions:delete_transaction", args=[transaction.pk]))
        self.assertEqual(response.status_code, 404)

    def test_list_show_only_logged_in_user_accounts_transactions(self):
        user2 = User.objects.create_user(
            username="testuser2", password="testpass", email="test2@example.com", first_name="Test", last_name="User2"
        )
        account = Account.objects.create(
            user=self.user, name="Test Account", type="checking", balance=100.00, currency="USD"
        )
        account2 = Account.objects.create(
            user=user2, name="Test Account 2", type="checking", balance=100.00, currency="USD"
        )
        transaction = Transaction.objects.create(
            account=account,
            date="2023-01-01",
            type="income",
            amount=50.00,
            description="Test transaction",
            category="Test category",
        )
        transaction2 = Transaction.objects.create(
            account=account2,
            date="2023-01-01",
            type="income",
            amount=50.00,
            description="Second transaction",
            category="Test category",
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse("transactions:transaction_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, transaction.description)
        self.assertNotContains(response, transaction2.description)