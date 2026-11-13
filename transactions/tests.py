from django.test import TestCase

from users.models import User
from .models import Transaction
from accounts.models import Account

# Create your tests here.
class TransactionTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account = Account.objects.create(
            user=User.objects.create_user(
                username="testuser", password="testpass", email="test@example.com", first_name="Test", last_name="User"
            ),
            name="Test Account",
            type="checking",
            balance=100.00,
            currency="USD",
        )
        cls.transaction = Transaction(
            account = cls.account,
            date = "2023-01-01",
            type = "income",
            amount = 50.00,
            description = "Test transaction",
            category = "Test category",
        )
        cls.transaction.save()

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.account, self.account)
        self.assertEqual(self.transaction.type, "income")
        self.assertEqual(self.transaction.amount, 50.00)
        self.assertEqual(self.transaction.description, "Test transaction")
        self.assertEqual(self.transaction.category, "Test category")

    def test_transaction_editing(self):
        # Test editing a transaction
        self.transaction.description = "Updated transaction"
        self.transaction.amount = 75.00
        self.transaction.save()

        updated_transaction = Transaction.objects.get(id=self.transaction.id)
        self.assertEqual(updated_transaction.description, "Updated transaction")
        self.assertEqual(updated_transaction.amount, 75.00)

    def test_transaction_deletion(self):
        self.transaction.delete()
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=self.transaction.id)