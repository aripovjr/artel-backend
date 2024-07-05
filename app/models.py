from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='products/', default="default/IMG_0024 2.JPG")
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
    discount_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Promo #{self.id}"

