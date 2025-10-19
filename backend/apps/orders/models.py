"""Order management models."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.apps.catalog.models import Product


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self) -> str:
        return f"{self.line1}, {self.city}"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        SHIPPED = "shipped", _("Shipped")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(Address, related_name="shipping_orders", on_delete=models.PROTECT)
    billing_address = models.ForeignKey(Address, related_name="billing_orders", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self) -> str:
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price
