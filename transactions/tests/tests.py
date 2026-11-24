from datetime import date
from decimal import Decimal

from django.db.models import ProtectedError
from django.test import TestCase

from accounts.models import Account
from transactions.models import Transaction
from users.models import User


class TransactionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        cls.account = Account.objects.create(
            user=cls.user,
            name="Test Account",
            type="checking",
            balance=Decimal("100.00"),
            currency="USD",
        )
        cls.transaction = Transaction.objects.create(
            account=cls.account,
            date=date(2023, 1, 1),
            type="income",
            amount=Decimal("50.00"),
            description="Test transaction",
            category="Test category",
        )

    def test_transaction_is_saved_to_database(self):
        # Read the row back with a fresh query, not the in-memory object.
        saved = Transaction.objects.get(pk=self.transaction.pk)

        self.assertEqual(saved.account, self.account)
        self.assertEqual(saved.date, date(2023, 1, 1))
        self.assertEqual(saved.type, "income")
        self.assertEqual(saved.amount, Decimal("50.00"))
        self.assertEqual(saved.description, "Test transaction")
        self.assertEqual(saved.category, "Test category")

    def test_editing_a_saved_transaction_is_refused(self):
        self.transaction.amount = Decimal("999.00")
        self.transaction.description = "Changed"

        # Only the call that should raise goes inside the block.
        with self.assertRaises(ValueError):
            self.transaction.save()

        # The refusal must leave the database untouched.
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, Decimal("50.00"))
        self.assertEqual(self.transaction.description, "Test transaction")

    def test_account_with_transactions_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.account.delete()

        self.assertTrue(Account.objects.filter(pk=self.account.pk).exists())
        self.assertTrue(Transaction.objects.filter(pk=self.transaction.pk).exists())

    def test_transaction_can_be_deleted(self):
        pk = self.transaction.pk
        self.transaction.delete()

        self.assertFalse(Transaction.objects.filter(pk=pk).exists())
