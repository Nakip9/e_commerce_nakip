from django.contrib import admin

from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username")
    inlines = [OrderItemInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "line1", "city", "country")
    search_fields = ("user__username", "line1", "city", "country")
