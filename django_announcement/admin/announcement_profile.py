from django.contrib.admin import register
from django.db.models import QuerySet
from django.http import HttpRequest

from django_announcement.admin.inlines import UserAudienceInline
from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models import UserAnnouncementProfile
from django_announcement.settings.conf import config
from django_announcement.utils.user_model import USERNAME_FIELD, get_username


@register(UserAnnouncementProfile, site=config.admin_site_class)
class UserAnnouncementProfileAdmin(BaseModelAdmin):
    autocomplete_fields = ["user", "audiences"]
    inlines = [UserAudienceInline]
    list_display = BaseModelAdmin.list_display + [
        "get_username",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["get_username"]
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

    def get_username(self, obj: UserAnnouncementProfile) -> str:
        """Retrieve the username from the related User model.

        Args:
            obj (User AnnouncementProfile): The instance of UserAnnouncementProfile
                for which the username is being retrieved.

        Returns:
            str: The username of the user if available; otherwise, returns an empty string.

        """
        return get_username(obj.user) if obj.user else ""

    get_username.short_description = "User"
