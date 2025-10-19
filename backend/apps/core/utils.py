"""Helper utilities for the Nakip backend."""
from __future__ import annotations

from django.utils.translation import gettext_lazy as _


def translated_label(en: str, ar: str) -> str:
    """Return a combined translated label for documentation or UI."""
    return _("%(english)s / %(arabic)s") % {"english": en, "arabic": ar}
