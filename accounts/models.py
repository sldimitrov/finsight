from django.db import models
from django.conf import settings


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit', 'Credit'),
        ('investment', 'Investment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    # Allowing negative balances
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"