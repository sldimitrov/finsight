from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),
    path("filter/", views.filter_transactions, name="filter_transactions"),
    path("<int:transaction_id>/", views.transaction_detail, name="transaction_detail"),
    path("<int:transaction_id>/delete/", views.delete_transaction, name="delete_transaction"),
]
