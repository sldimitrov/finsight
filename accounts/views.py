from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import AccountForm
from .models import Account


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    next_page = reverse_lazy("accounts:index")


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@login_required
def index(request):
    accounts = Account.objects.filter(user=request.user, is_active=True).order_by("name")
    return render(request, "accounts/account_list.html", {"accounts": accounts})


@login_required
def create(request):
    form = AccountForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return redirect("accounts:detail", account_id=account.pk)

    return render(request, "accounts/account_form.html", {"form": form, "title": "Create account"})


@login_required
def detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return render(request, "accounts/account_detail.html", {"account": account})


@login_required
def update(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    form = AccountForm(request.POST if request.method == "POST" else None, instance=account)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("accounts:detail", account_id=account.pk)

    return render(
        request,
        "accounts/account_form.html",
        {"form": form, "account": account, "title": "Edit account"},
    )


@login_required
@require_POST
def deactivate(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    account.is_active = False
    account.save(update_fields=("is_active",))
    return redirect("accounts:index")
