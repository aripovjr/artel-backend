from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_view(), name='index'),
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
    path('api/products/<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('api/products/<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='product-update'),
    path('api/products/<int:pk>/delete/', views.ProductDestroyAPIView.as_view(), name='product-delete'),
    path('api/get_product_by_category/', views.GetProductByCategory.as_view()),
    path('api/get_all_categories/', views.GetAllCategories.as_view()),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
