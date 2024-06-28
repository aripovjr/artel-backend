from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.status import HTTP_201_CREATED

from .models import Product, Category, Order, Promo
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderGetSerializer, PromoSerializer
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description="Search by Product name",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        product_name = self.request.query_params.get('q', None)
        if product_name:
            return Product.objects.filter(name__icontains=product_name)
        else:
            return Product.objects.all()


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_name = serializer.validated_data["category"]["name"]
        category = get_object_or_404(Category, name=category_name)
        serializer.validated_data["category"] = category
        product = Product.objects.create(**serializer.validated_data)
        return Response(self.get_serializer(product).data, status=HTTP_201_CREATED)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetAllCategories(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetProductByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Search by Category name",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        category_name = self.request.query_params.get('category', None)
        if category_name is not None:
            category = get_object_or_404(Category, name=category_name)
            return Product.objects.filter(category=category)
        else:
            return Product.objects.all()


# CRUD FOR ORDER

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        order_count = serializer.validated_data['count']

        # Check if there is enough product amount
        if product.amount < order_count:
            raise ValidationError('Not enough product in stock.')

        # Subtract the order count from the product amount
        product.amount -= order_count
        product.save()

        # Save the order
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderGet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    pagination_class = ProductPagination


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# CRUD FOR PROMO
class PromoCreateAPIView(generics.CreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class PromoGetAPIView(generics.ListAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    pagination_class = ProductPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q', openapi.IN_QUERY, description="Search by Promo name",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        promo_name = self.request.query_params.get('q', None)
        if promo_name:
            return Promo.objects.filter(name__icontains=promo_name)
        else:
            return Product.objects.all()


class PromoDeleteAPIView(generics.DestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
