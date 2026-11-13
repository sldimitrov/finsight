from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "type", "amount", "description", "account")
    list_filter = ("type", "date", "account")
    search_fields = ("description",)
