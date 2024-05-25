from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ProductListView,
    ProductDetailView, ProductsByCategoryView, ProductStatsView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'product-list/',
        ProductListView.as_view(),
        name='product-list-view'
    ),
    path(
        'products/<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),
    path(
        'products/category/<str:category_name>/',
        ProductsByCategoryView.as_view(),
        name='products-by-category'
    ),
    path('product-stats/', ProductStatsView.as_view(), name='product-stats'),
]
