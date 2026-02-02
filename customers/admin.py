from django.contrib import admin
from .models import Customer, Address

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'street', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
    search_fields = ('street', 'city', 'state', 'postal_code', 'country')
    list_filter = ('country', 'created_at', 'updated_at')
