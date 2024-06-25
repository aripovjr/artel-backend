from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_view(), name='index'),
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('api/products/<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('api/products/<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='product-update'),
    path('api/products/<int:pk>/delete/', views.ProductDestroyAPIView.as_view(), name='product-delete'),

]
