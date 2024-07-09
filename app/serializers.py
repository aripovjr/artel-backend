from datetime import date
# from datetime import timezone
from django.utils import timezone
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from .models import Product, Category, Order, Promo, Color
from accounts.serializers import UserSerializer


class PromoSerializer(serializers.ModelSerializer):
    # discount_status = serializers.SerializerMethodField()

    class Meta:
        model = Promo
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = Color
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    colors = ColorSerializer(many=True, required=False)
    promo = PromoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        category_name = validated_data.pop('category')['name']
        category = get_object_or_404(Category, name=category_name)

        colors_data = validated_data.pop('colors', [])
        promos_data = validated_data.pop('promo', [])

        product = Product.objects.create(category=category, **validated_data)
        for color_data in colors_data:
            c = Color.objects.create(**color_data)
            product.colors.add(c)
            product.save()

        for promo_data in promos_data:
            promo_data.pop("product")
            Promo.objects.create(product=product, **promo_data)

        return product

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


