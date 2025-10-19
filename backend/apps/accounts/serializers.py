"""Serializers for user management."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        read_only_fields = ("id",)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_confirm")

    def validate_email(self, value):  # type: ignore[override]
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_("Email already registered"))
        return value

    def validate(self, attrs):  # type: ignore[override]
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": _("Passwords do not match")})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):  # type: ignore[override]
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
