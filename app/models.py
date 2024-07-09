from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from drf_extra_fields.fields import Base64ImageField


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=255, null=True, blank=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)
    photo = models.ImageField(upload_to='products/', default="default/IMG_0024 2.JPG")
    # photo = Base64ImageField(allow_null=True, required=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    colors = models.ManyToManyField(Color, blank=True, related_name='colors')

    def __str__(self):
        return self.name


class Order(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default="korilmagan")

    def __str__(self):
        return str(self.admin)


class Promo(models.Model):
    bonus = models.IntegerField(default=0)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name="promos")
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    is_extra = models.BooleanField(default=False)

    def __str__(self):
        return f"Promo #{self.id}"

