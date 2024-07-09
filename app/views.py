from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.status import HTTP_201_CREATED

from .models import Product, Category, Order, Promo, Color
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderGetSerializer, PromoSerializer, \
    ColorSerializer
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
                              type=openapi.TYPE_STRING),
            openapi.Parameter("category", openapi.IN_QUERY, description="Search by Product category", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        product_name = self.request.query_params.get('q', None)
        product_category = self.request.query_params.get("category", None)
        if product_name:
            return Product.objects.filter(name__icontains=product_name)

        if product_category:
            return Product.objects.filter(category__name__icontains=product_category)

        return Product.objects.all()




class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     product = serializer.save()
    #     return Response(self.get_serializer(product).data, status=HTTP_201_CREATED)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get("pk"))
        color_data = request.data.pop("colors", [])
        promo_data = request.data.pop("promo", [])

        if color_data:
            for data in color_data:
                id = data.get("id", False)
                if not id:
                    c = ColorSerializer(data=data)
                    c.is_valid(raise_exception=True)
                    c2 = c.save()
                    product.colors.add(c2)
                    product.save()
                else:
                    color_instance = get_object_or_404(Color, id=id)
                    color_serializer = ColorSerializer(instance=color_instance, data=data, partial=True)
                    color_serializer.is_valid(raise_exception=True)
                    color_serializer.save()

        # serializer = self.get_serializer(instance=product, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        if promo_data:
            for data in promo_data:
                id = data.get('id', False)
                data.pop('product')
                if not id:
                    Promo.objects.create(product=product, **data)
                else:
                    promo_instance = get_object_or_404(Promo, id=id, product=product)
                    promo_serializer = PromoSerializer(instance=promo_instance, data=data, partial=True)
                    promo_serializer.is_valid(raise_exception=True)
                    promo_serializer.save()

        serializer = self.get_serializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


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
            return Promo.objects.all()


class PromoDeleteAPIView(generics.DestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class PromoUpdateAPIView(generics.UpdateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class PromoRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class ColorGetAPIView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorUpdateAPIView(generics.UpdateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorDeleteAPIView(generics.DestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
