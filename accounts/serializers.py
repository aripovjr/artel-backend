from rest_framework import serializers
from .models import CustomUser


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['groups', 'user_permissions', "is_admin", "is_active", "is_staff", "is_superuser", "last_login", "password"]
        extra_kwargs = {
            "password": {"read_only": True},
            "phone_number": {"read_only": True},
        }
