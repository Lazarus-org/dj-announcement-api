from typing import Any, Optional

from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db.models import ForeignKey
from django.http import HttpRequest


class ForeignKeyRawIdWidgetMixin:
    """A mixin to override form field for foreign keys to use
    ForeignKeyRawIdWidget."""

    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> Optional[Any]:
        """Override the default form field for foreign keys to use
        ForeignKeyRawIdWidget."""
        # Assign ForeignKeyRawIdWidget to the widget option
        kwargs.setdefault(
            "widget",
            ForeignKeyRawIdWidget(
                db_field.remote_field, self.admin_site, using=kwargs.get("using")
            ),
        )

        # Set queryset if not provided in kwargs
        kwargs.setdefault(
            "queryset", self.get_field_queryset(kwargs.get("using"), db_field, request)
        )

        return db_field.formfield(**kwargs)
