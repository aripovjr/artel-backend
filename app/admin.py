from django.contrib import admin
from .models import Category, Product, Order, Promo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Promo)
