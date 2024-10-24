from django.contrib.admin import TabularInline
from django.db.models import QuerySet
from django.http import HttpRequest

from django_announcement.mixins.admin.form_fields import ForeignKeyRawIdWidgetMixin
from django_announcement.mixins.admin.permission import InlinePermissionControlMixin


class BaseTabularInline(
    InlinePermissionControlMixin, ForeignKeyRawIdWidgetMixin, TabularInline
):
    """Base tabular inline admin interface with common functionality for all
    inlines.

    This class serves as the foundation for all inlines. Any tabular inline can inherit from this
    class to reuse its common functionality.

    Attributes:
        extra: Number of empty forms to display by default.
        max_num: Maximum number of forms allowed in the inline..

    """

    extra = 0
    max_num = 10


class BaseAudienceInline(BaseTabularInline):
    """Base inline admin interface for managing models with audience
    relationships.

    This class serves as a base for inlines that handle models with foreign key relationships
    to audience-related models. It optimizes performance by selecting related fields and
    allows customization of widget behavior.

    Attributes:
        autocomplete_fields: Fields that support autocomplete for admin.

    """

    autocomplete_fields = ["audience"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Optimize the queryset by selecting related fields.

        Args:
            request: The current HTTP request.

        Returns:
            QuerySet with optimized performance by selecting related fields.

        """
        return super().get_queryset(request).select_related("audience")
