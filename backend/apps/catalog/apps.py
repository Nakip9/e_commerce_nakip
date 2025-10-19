from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.catalog"
    verbose_name = _("Catalog")

    def ready(self) -> None:  # pragma: no cover - import for side effects
        from . import translation  # noqa: F401
        return super().ready()
