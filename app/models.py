from django.db import models
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    amount = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='products/', default="default/IMG_0024 2.JPG")

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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="promos/", default='default/IMG_0024 2.JPG')

    def __str__(self):
        return self.name
