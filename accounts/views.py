from django.http import HttpResponse

from .models import Account


def index(request):
    return HttpResponse("Hello, world. You're at the accounts index.")

def detail(request, account_id):
    account = Account.objects.get(id=account_id)

    return HttpResponse(f"Hello, world. You're at the accounts detail page for account {account.name}."
                        f" Account type: {account.type}, Balance: {account.balance} {account.currency}.")
