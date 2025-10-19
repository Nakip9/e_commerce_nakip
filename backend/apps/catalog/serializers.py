"""Serializers for catalog resources."""
from __future__ import annotations

from rest_framework import serializers

from backend.apps.core.serializers import BaseModelSerializer, TranslatedFieldsMixin

from .models import Category, Product, ProductImage, Review


class CategorySerializer(BaseModelSerializer, TranslatedFieldsMixin):
    class Meta(BaseModelSerializer.Meta):
        model = Category
        fields = BaseModelSerializer.Meta.fields + ("name", "description", "slug")

    def to_representation(self, instance):  # type: ignore[override]
        data = super().to_representation(instance)
        data.update(self.get_translated_fields(instance, ["name", "description"]))
        return data


class ProductImageSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = ProductImage
        fields = BaseModelSerializer.Meta.fields + ("image", "alt_text")


class ReviewSerializer(BaseModelSerializer):
    user = serializers.StringRelatedField()

    class Meta(BaseModelSerializer.Meta):
        model = Review
        fields = BaseModelSerializer.Meta.fields + ("user", "rating", "title", "body")


class ProductSerializer(BaseModelSerializer, TranslatedFieldsMixin):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Product
        fields = BaseModelSerializer.Meta.fields + (
            "category",
            "category_id",
            "name",
            "description",
            "price",
            "stock",
            "sku",
            "is_active",
            "featured",
            "image",
            "images",
            "reviews",
        )

    def to_representation(self, instance):  # type: ignore[override]
        data = super().to_representation(instance)
        data.update(self.get_translated_fields(instance, ["name", "description"]))
        return data


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "sku",
            "is_active",
            "featured",
            "image",
            "category",
        )
