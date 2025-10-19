"""Custom permission classes."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Allow read-only access to everyone but restrict writes to staff."""

    def has_permission(self, request, view):  # type: ignore[override]
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
