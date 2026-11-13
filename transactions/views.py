from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from django.db import transaction
from .models import Transaction


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(account__user=request.user)
    return render(request, "transactions/transaction_list.html", {"transactions": transactions})


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, id=transaction_id, account__user=request.user
    )
    return render(request, "transactions/transaction_detail.html", {"transaction": transaction})


@login_required
def filter_transactions(request, transaction_type=None):
    transaction_type = request.GET.get("type", transaction_type)
    transactions = Transaction.objects.filter(account__user=request.user)
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    return render(request, "transactions/transaction_list.html", {"transactions": transactions})


@login_required
@transaction.atomic
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, id=transaction_id, account__user=request.user
    )
    if request.method == "POST":
        transaction.date = request.POST.get("date")
        transaction.description = request.POST.get("description")
        transaction.category = request.POST.get("category")

        new_type = request.POST.get("type")
        new_amount = request.POST.get("amount")

        # TODO: Handle change type and amount correctly, adjusting the account balance accordingly
        # Step 1: Undo the operation
        if transaction.type == "income":
            transaction.account.balance -= transaction.amount
        elif transaction.type == "expense":
            transaction.account.balance += transaction.amount

        # Step 2: Apply the new operation
        if new_type == "income":
            transaction.account.balance += float(new_amount)
        elif new_type == "expense":
            transaction.account.balance -= float(new_amount)

        transaction.type = new_type
        transaction.amount = new_amount

        transaction.save()
        return redirect("transactions:transaction_detail", transaction_id=transaction.id)
    return render(request, "transactions/edit_transaction.html", {"transaction": transaction})


@login_required
@transaction.atomic
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, id=transaction_id, account__user=request.user
    )
    if request.method == "POST":
        transaction.delete()

        if transaction.type == "income":
            transaction.account.balance -= transaction.amount
        elif transaction.type == "expense":
            transaction.account.balance += transaction.amount
        transaction.account.save(update_fields=("balance",))

        return redirect("transactions:transaction_list")
    return render(request, "transactions/delete_transaction.html", {"transaction": transaction})
