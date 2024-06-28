from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from .models import Product, Category, Order, Promo
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    photo = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        # Update the category
        if 'category' in validated_data:
            cat = validated_data.pop('category')['name']
            category = get_object_or_404(Category, name=cat)
            instance.category = category

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class OrderGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    admin = UserSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class PromoSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = Promo
        fields = "__all__"
