from django.contrib import admin
from .models import Order, OrderItem

# Create an inline class for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

# Register Order with OrderItem inline
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'wilaya', 'created_at', 'total_amount')
    list_filter = ('created_at', 'wilaya')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('session_id', 'created_at', 'total_amount')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        ('Address Information', {
            'fields': ('wilaya', 'daira', 'address')
        }),
        ('Order Details', {
            'fields': ('notes', 'created_at', 'total_amount', 'session_id')
        }),
    )
