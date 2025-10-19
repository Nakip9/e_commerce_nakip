"""Model translations using django-modeltranslation."""
from modeltranslation.translator import TranslationOptions, translator

from .models import Category, Product


class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description")


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
