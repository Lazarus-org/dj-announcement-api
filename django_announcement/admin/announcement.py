from django.contrib.admin import register
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from django_announcement.admin.inlines import AudienceInline
from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models import Announcement
from django_announcement.settings.conf import config


@register(Announcement, site=config.admin_site_class)
class AnnouncementAdmin(BaseModelAdmin):
    autocomplete_fields = ["category"]
    inlines = [AudienceInline]
    list_display = BaseModelAdmin.list_display + [
        "title",
        "category",
        "created_at",
        "expires_at",
    ]
    list_display_links = ["title"]
    list_filter = BaseModelAdmin.list_filter + ["category"]
    search_fields = BaseModelAdmin.search_fields + [
        "title",
        "content",
        "audience__name",
    ]
    ordering = BaseModelAdmin.ordering + ["-expires_at"]
    fieldsets = [
        (
            None,
            {
                "fields": ("title", "content", "category", "attachment"),
                "description": _(
                    "Primary fields related to the announcement, including the title, content, category and attachment."
                ),
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": ("published_at", "expires_at"),
                "description": _(
                    "Details regarding the announcement's publish and expiration date."
                ),
            },
        ),
    ] + BaseModelAdmin.fieldsets

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Override the get_queryset method to select related fields for
        performance optimization.

        Args:
            request: The current HTTP request.

        Returns:
            A queryset with selected related fields for performance optimization.

        """
        return super().get_queryset(request).select_related("category")
