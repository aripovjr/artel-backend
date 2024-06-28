from django.contrib import admin
from .models import Category, Product, Order, Promo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Promo)
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("name", "model", "category", "price", "discount", "amount")
#     list_filter = ("category",)
#     search_fields = ("name", "model", "description")
#
#     fields = ('name', 'model', 'category', 'price', 'discount', 'amount', 'description')
