from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "balance", "currency", "user")
    search_fields = ("name", "type", "user__username")
    list_filter = ("type", "currency")