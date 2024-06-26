from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Include any other fields you want to display


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    # category_id = serializers.PrimaryKeyRelatedField(
    #     source='category', queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = '__all__'
