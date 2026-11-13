from django.db import models
from accounts.models import Account


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
        ("adjustment", "Adjustment"),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    source_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="source_transactions", blank=True, null=True
    )
    destination_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="destination_transactions", blank=True, null=True
    )

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description}"

    def save(self, *args, **kwargs):
        # Make sure the Transaction cannot be edited
        if self.pk is not None:
            raise ValueError("Transactions cannot be edited once created.")
        super().save(*args, **kwargs)