from django.contrib import admin
from .models import Product, Category, ReservedProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at', 'parent')

@admin.register(ReservedProduct)
class ReservedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'reserved_quantity', 'reserved_at', 'expires_at')
    search_fields = ('product__name',)
    list_filter = ('reserved_at', 'expires_at')
