from django.contrib import admin
from .models import Category, Product, Order, Promo, Color
from django import forms
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class PromoTabular(admin.TabularInline):
    model = Promo
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [PromoTabular]


# admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Promo)


class ColorAdminForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'hex_code': forms.TextInput(attrs={'type': 'color'})
        }


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorAdminForm
