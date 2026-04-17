from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'status', 'is_paid', 'total_price', 'created')
    list_filter = ('status', 'is_paid', 'payment_method')
    list_editable = ('status', 'is_paid')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created', 'updated', 'total_price')
    inlines = [OrderItemInline]
