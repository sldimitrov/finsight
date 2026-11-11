from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.AccountLoginView.as_view(), name="login"),
    path("logout/", views.AccountLogoutView.as_view(), name="logout"),
    path("create/", views.create, name="create"),
    path("<int:account_id>/", views.detail, name="detail"),
    path("<int:account_id>/edit/", views.update, name="update"),
    path("<int:account_id>/deactivate/", views.deactivate, name="deactivate"),
]