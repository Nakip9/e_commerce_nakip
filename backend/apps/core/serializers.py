"""Common serializer mixins."""
from rest_framework import serializers


class TranslatedFieldsMixin:
    """Include translated fields for modeltranslation-enabled models."""

    def get_translated_fields(self, instance, fields: list[str]) -> dict[str, str | None]:
        data: dict[str, str | None] = {}
        for field in fields:
            data[field] = getattr(instance, field)
            data[f"{field}_ar"] = getattr(instance, f"{field}_ar", None)
            data[f"{field}_en"] = getattr(instance, f"{field}_en", None)
        return data


class BaseModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        fields: tuple[str, ...] = ("id", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
