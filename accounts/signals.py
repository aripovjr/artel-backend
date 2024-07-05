from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from app.models import Product, Promo


@receiver(post_save, sender=CustomUser)
def assign_default_permissions(sender, instance, created, **kwargs):
    if created and instance.admin_type == "1":
        dealer_group, group = Group.objects.get_or_create(name='Admin')
        if group:
            app_label = 'app'
            models = ['product', 'promo']
            permissions = ['add', 'change', 'delete', 'view']

            for model in models:
                for perm in permissions:
                    codename = f"{perm}_{model}"
                    try:
                        permission = Permission.objects.get(codename=codename, content_type__app_label=app_label)
                        dealer_group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        print(f"Permission {codename} not found")
            dealer_group.save()

        instance.groups.add(dealer_group.id)

        # instance.user_permissions.add(*dealer_group.permissions.all())

        instance.is_admin = True
        instance.is_superuser = True
        instance.set_password(instance.password)
        instance.save()
