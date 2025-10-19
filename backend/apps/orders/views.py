"""Viewsets for order management and checkout."""
from __future__ import annotations

from rest_framework import mixins, permissions, viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # type: ignore[override]
        return Order.objects.filter(user=self.request.user).select_related(
            "shipping_address", "billing_address"
        ).prefetch_related("items__product")

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save()
