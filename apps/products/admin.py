from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'regular_price', 'discount_price', 'stock', 'description'
    )
    search_fields = ('name', 'description')
    list_filter = ('categories',)
    filter_horizontal = ('categories',)
    ordering = ('name',)
    fields = (
        'name', 'regular_price', 'discount_price',
        'stock', 'description', 'categories'
    )
