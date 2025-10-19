"""Project URL configuration."""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("backend.apps.accounts.urls")),
    path("api/catalog/", include("backend.apps.catalog.urls")),
    path("api/", include("backend.apps.orders.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
