"""Viewsets for catalog management."""
from __future__ import annotations

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.apps.core.filters import ProductFilter
from backend.apps.core.permissions import IsAdminOrReadOnly

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductSerializer, ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    filterset_fields = ("slug",)
    search_fields = ("name", "description")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = ProductFilter
    search_fields = ("name", "description", "sku")
    ordering_fields = ("price", "created_at", "updated_at")

    def get_serializer_class(self):  # type: ignore[override]
        if self.action == "list":
            return ProductListSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def search(self, request, *args, **kwargs):  # type: ignore[override]
        query = request.query_params.get("q", "")
        queryset = self.filter_queryset(self.get_queryset())
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(name_ar__icontains=query)
                | Q(name_en__icontains=query)
                | Q(description__icontains=query)
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def reviews(self, request, pk=None):  # type: ignore[override]
        product = self.get_object()
        if request.method == "POST":
            serializer = ReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": serializer.validated_data["rating"],
                    "title": serializer.validated_data["title"],
                    "body": serializer.validated_data["body"],
                },
            )
        reviews = product.reviews.filter(is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
