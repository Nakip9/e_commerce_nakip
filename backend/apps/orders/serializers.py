"""Serializers for order and checkout APIs."""
from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from backend.apps.catalog.models import Product

from .models import Address, Order, OrderItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "phone_number",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):  # type: ignore[override]
        user = self.context["request"].user
        return Address.objects.create(user=user, **validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "quantity", "unit_price")
        read_only_fields = ("id", "unit_price", "product_name")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()
    billing_address = AddressSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "subtotal",
            "shipping_cost",
            "total",
            "items",
            "shipping_address",
            "billing_address",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "status", "subtotal", "total", "created_at", "updated_at")

    def create(self, validated_data):  # type: ignore[override]
        items_data = validated_data.pop("items")
        shipping_address_data = validated_data.pop("shipping_address")
        billing_address_data = validated_data.pop("billing_address")
        request = self.context["request"]
        shipping_cost_raw = validated_data.pop("shipping_cost", 0)
        shipping_cost = Decimal(str(shipping_cost_raw))

        with transaction.atomic():
            shipping_address = AddressSerializer(data=shipping_address_data, context=self.context)
            shipping_address.is_valid(raise_exception=True)
            shipping_address_obj = shipping_address.save()

            billing_address = AddressSerializer(data=billing_address_data, context=self.context)
            billing_address.is_valid(raise_exception=True)
            billing_address_obj = billing_address.save()

            subtotal = Decimal("0")
            order = Order.objects.create(
                user=request.user,
                subtotal=Decimal("0"),
                shipping_cost=shipping_cost,
                total=Decimal("0"),
                shipping_address=shipping_address_obj,
                billing_address=billing_address_obj,
            )

            order_items = []
            for item in items_data:
                product: Product = item["product"]
                quantity = item.get("quantity", 1)
                unit_price = product.price
                subtotal += unit_price * quantity
                order_items.append(
                    OrderItem(order=order, product=product, quantity=quantity, unit_price=unit_price)
                )
                product.stock = max(product.stock - quantity, 0)
                product.save(update_fields=["stock"])
            OrderItem.objects.bulk_create(order_items)

            order.subtotal = subtotal
            order.total = subtotal + order.shipping_cost
            order.save(update_fields=["subtotal", "total"])

            return order
