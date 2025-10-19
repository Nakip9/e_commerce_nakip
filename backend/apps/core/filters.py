"""Common filters used across APIs."""
from django_filters import rest_framework as filters

from backend.apps.catalog.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "in_stock"]

    def filter_in_stock(self, queryset, name, value):  # type: ignore[override]
        if value is None:
            return queryset
        return queryset.filter(stock__gt=0) if value else queryset.filter(stock__lte=0)
