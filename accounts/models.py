from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, phone_number, password=None, fullname=None):

        if not phone_number:
            raise ValueError("Please enter your phone number")

        user = self.model(
            phone_number=phone_number,
            password=phone_number
        )
        user.set_password(phone_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, fullname=None):
        user = self.create_user(
            phone_number=phone_number,
            password=phone_number
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


PHONE_REGEX = RegexValidator(
    regex=r"^\+998([0-9][0-9]|99)\d{7}$",
    message="Please provide valid phone number"
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    admin_types = (
        ("0", "bloklangan"),
        ("1", "oddiy"),
        ("2", "admin qoshish"),
        ("3", "mahsulot qoshish")
    )
    fullname = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=21, unique=True)
    info = models.TextField(default="")
    admin_type = models.CharField(choices=admin_types, max_length=255, default="1")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


