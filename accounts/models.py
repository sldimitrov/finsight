from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("A username is required.")
        if not email:
            raise ValueError("An email address is required.")

        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("A superuser must have is_superuser=True.")

        return self.create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    base_currency = models.CharField(max_length=3, default='BGN')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit', 'Credit'),
        ('investment', 'Investment'),
    ]

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    # Allowing negative balances
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"