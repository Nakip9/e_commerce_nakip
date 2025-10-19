"""Catalog models representing the product catalog."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/main", blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        ordering = ("product", "id")

    def __str__(self) -> str:
        return f"{self.product} image"


class Review(TimeStampedModel):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ("-created_at",)
        unique_together = ("product", "user")

    def __str__(self) -> str:
        return f"{self.product} - {self.rating}"
