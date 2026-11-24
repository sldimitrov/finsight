from django.core.management import BaseCommand

import datetime
from users.models import User
from accounts.models import Account
from transactions.models import Transaction

class Command(BaseCommand):
    help = "Seeds the database with data for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=1000
        )

        parser.add_argument(
            "--clear",
            default=False
        )

    def handle(self, *args, **kwargs):
        # Create a superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="test@gmail.com",
                password="adminpass",
                first_name="Admin",
                last_name="User",
            )

        account = Account.objects.create(
            user=User.objects.get(username="admin"),
            name="Admin Account",
            type="checking",
            balance=1000.00,
            currency="USD",
        )

        transactions = [
            Transaction(account=account, description=f"Transaction {i}", amount=100.00, date=datetime.datetime.now().date(), type="income") for i in range(kwargs["count"])
        ]

        Transaction.objects.bulk_create(transactions, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {kwargs['count']} transactions."))

        if kwargs["clear"]:
            self.stdout.write("Clearing all data...")
