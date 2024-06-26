from django.db import models


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
    description = models.TextField(default="")
    photo = models.ImageField(upload_to='products/', default="default/IMG_0024 2.JPG")

    def __str__(self):
        return self.name
