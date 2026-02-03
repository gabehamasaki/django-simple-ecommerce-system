from django.contrib import admin
from .models import Order, OrderItem


class ProductInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount', 'transport_status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'customer__name')
    list_filter = ('transport_status', 'payment_status', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'order_number', 'customer', 'total_amount', 'transport_status', 'payment_status', 'created_at', 'address_snapshot', 'address')
    inlines = [ProductInline]

@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at')
    search_fields = ('order__order_number', 'product__name')
    list_filter = ('created_at',)
    readonly_fields = ('order', 'product', 'quantity', 'price', 'created_at', 'updated_at')
