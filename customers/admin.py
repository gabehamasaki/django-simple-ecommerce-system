from django.contrib import admin
from .models import Customer, Address

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    #readonly_fields = ('street', 'city', 'state', 'postal_code', 'country')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj = ...):
        return False

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [AddressInline]

    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'addresses_count',
        'created_at',
        'updated_at'
    )
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at', 'updated_at')

    def addresses_count(self, obj):
        return obj.addresses.count()
    addresses_count.short_description = 'Number of Addresses'

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'street', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    search_fields = ('street', 'city', 'state', 'postal_code', 'country')
    list_filter = ('country', 'created_at', 'updated_at', 'customer')


class CustomerInline(admin.StackedInline):
    model = Customer
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
