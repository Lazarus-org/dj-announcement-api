from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.admin.form_fields import ForeignKeyRawIdWidgetMixin
from django_announcement.mixins.admin.permission import AdminPermissionControlMixin


class BaseModelAdmin(
    AdminPermissionControlMixin, ForeignKeyRawIdWidgetMixin, ModelAdmin
):
    """Base class for all ModelAdmin classes in the Django admin interface.

    This class provides common functionalities and configurations that can
    be reused across different admin models, promoting consistency and
    reducing code duplication. It includes settings for display options,
    pagination, filtering, ordering, and read-only fields.

    Attributes:
        list_display (list): Fields to be displayed in the list view of the admin.
        list_per_page (int): Number of items to display per page in the list view.
        list_filter (list): Fields to be used for filtering the list view.
        ordering (list): Default ordering of items in the list view.
        readonly_fields (list): Fields that should be read-only in the admin form.
        search_fields (list): Fields to be searchable in the admin interface.
        fieldsets (list): Grouping of fields in the admin form with optional descriptions.

    Usage:
        Subclass `BaseModelAdmin` to create custom admin interfaces for your models,
        inheriting the common configurations and functionalities provided by this base class.

    """

    list_display = ["id"]
    list_per_page = 10
    list_filter = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["id"]
    fieldsets = [
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "description": _(
                    "System-generated timestamps indicating when the object was created and last updated."
                ),
                "classes": ("collapse", "wide"),
            },
        ),
    ]
