from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from transactions.models import Transaction
from users.models import User
from django.db.models import ProtectedError


class TransactionBalanceViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="alice",
            password="testpass",
            email="alice@example.com",
            first_name="Alice",
            last_name="Tester",
        )
        cls.account = Account.objects.create(
            user=cls.user,
            name="Checking",
            type="checking",
            balance=Decimal("100.00"),
            currency="USD",
        )

    def setUp(self) -> None:
        # Log in without going through the login form.
        self.client.force_login(self.user)

    def test_income_increases_balance(self):
        url = reverse("accounts:create_transaction", args=[self.account.pk])

        # Field names must match TransactionForm.Meta.fields.
        response = self.client.post(
            url,
            {
                "date": "2026-01-15",
                "type": "income",
                "amount": "50.00",
                "description": "Salary",
                "category": "Work",
            },
        )

        self.assertRedirects(response, reverse("accounts:detail", args=[self.account.pk]))

        # The view changed the row in the DB; our in-memory object is stale until we reload it.
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("150.00"))

        self.assertEqual(Transaction.objects.filter(account=self.account).count(), 1)

    def test_expense_decreases_balance(self):
        url = reverse("accounts:create_transaction", args=[self.account.pk])

        response = self.client.post(
            url,
            {
                "date": "2026-01-16",
                "type": "expense",
                "amount": "30.00",
                "description": "Groceries",
                "category": "Food",
            },
        )
        self.assertRedirects(response, reverse("accounts:detail", args=[self.account.pk]))

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("70.00"))

        self.assertEqual(Transaction.objects.filter(account=self.account).count(), 1)

    def test_delete_transaction_updates_balance(self):
        # Create a transaction to delete later
        url = reverse("accounts:create_transaction", args=[self.account.pk])

        # Field names must match TransactionForm.Meta.fields.
        response = self.client.post(
            url,
            {
                "date": "2026-01-15",
                "type": "income",
                "amount": "20.00",
                "description": "Freelance work",
                "category": "Work",
            },
        )

        self.assertRedirects(response, reverse("accounts:detail", args=[self.account.pk]))

        # The view changed the row in the DB; our in-memory object is stale until we reload it.
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("120.00"))

        # Delete the transaction
        transaction = Transaction.objects.get(account=self.account)
        delete_url = reverse("transactions:delete_transaction", args=[transaction.pk])

        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("transactions:transaction_list"))

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("100.00"))

    def test_account_with_transactions_cannot_be_deleted(self):
        # Create a transaction associated with the account
        Transaction.objects.create(
            account=self.account,
            date="2026-01-18",
            type="income",
            amount=Decimal("10.00"),
            description="Gift",
            category="Other",
        )

        with self.assertRaises(ProtectedError):
            self.account.delete()

        self.assertTrue(Account.objects.filter(pk=self.account.pk).exists())
        self.assertTrue(Transaction.objects.filter(account=self.account).exists())