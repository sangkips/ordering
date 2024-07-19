from django.contrib import admin

from apps.orders.models import Item, Order, OrderDetail

# Register your models here.


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at"]
    list_filter = ["price", "created_at", "name"]


@admin.register(OrderDetail)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "quantity", "total"]
    list_filter = ["order", "item", "quantity", "created_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "payment_method", "created_at"]
    list_filter = ["customer", "created_at"]
