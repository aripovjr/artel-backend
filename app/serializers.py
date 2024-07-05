from datetime import date
# from datetime import timezone
from django.utils import timezone
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from .models import Product, Category, Order, Promo, Color
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
        if 'category' in validated_data:
            cat = validated_data.pop('category')['name']
            category = get_object_or_404(Category, name=cat)
            instance.category = category

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_date = date.today()
        promos_for_today = instance.promos.filter(from_date__lte=current_date, to_date__gte=current_date)
        representation['promo'] = PromoSerializer(promos_for_today, many=True).data

        color_for_product = instance.colors.all()
        representation['colors'] = ColorSerializer(color_for_product, many=True).data
        return representation


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
    # discount_status = serializers.SerializerMethodField()

    class Meta:
        model = Promo
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"
