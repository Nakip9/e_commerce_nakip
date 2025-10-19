from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "description")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "featured")
    list_filter = ("category", "is_active", "featured")
    search_fields = ("name", "description", "sku")
    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved")
    search_fields = ("product__name", "user__username", "title")
