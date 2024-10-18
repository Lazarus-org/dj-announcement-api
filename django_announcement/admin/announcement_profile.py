from django.contrib.admin import register
from django.db.models import QuerySet
from django.http import HttpRequest

from django_announcement.admin.inlines import UserAudienceInline
from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models import UserAnnouncementProfile
from django_announcement.utils.user_model import USERNAME_FIELD


@register(UserAnnouncementProfile)
class UserAnnouncementProfileAdmin(BaseModelAdmin):
    autocomplete_fields = ["user", "audiences"]
    inlines = [UserAudienceInline]
    list_display = BaseModelAdmin.list_display + [
        f"user__{USERNAME_FIELD}",
        "created_at",
        "updated_at",
    ]
    list_display_links = [f"user__{USERNAME_FIELD}"]
    search_fields = BaseModelAdmin.search_fields + [
        f"user__{USERNAME_FIELD}",
        "user__id",
        "audiences__name",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("user",),
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
        return super().get_queryset(request).select_related("user")
