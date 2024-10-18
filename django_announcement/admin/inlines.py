from django.contrib.admin import TabularInline
from django.db.models import QuerySet
from django.http import HttpRequest

from django_announcement.models.user_audience import UserAudience
from django_announcement.models.audience_announce import AudienceAnnouncement


class AudienceInline(TabularInline):
    """Inline admin interface for AudienceAnnouncement model.

    Attributes:
        model: The model associated with this inline.
        extra: Number of empty forms to display.

    """

    autocomplete_fields = ("audience",)
    model = AudienceAnnouncement
    extra = 0

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Override the get_queryset method to select related fields for
        performance optimization.

        Args:
            request: The current HTTP request.

        Returns:
            A queryset with selected related fields for performance optimization.

        """
        return super().get_queryset(request).select_related("audience")


class UserAudienceInline(TabularInline):
    """Inline admin interface for UserAudience model.

    Attributes:
        model: The model associated with this inline.
        extra: Number of empty forms to display.

    """

    autocomplete_fields = ("audience",)
    model = UserAudience
    extra = 0

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Override the get_queryset method to select related fields for
        performance optimization.

        Args:
            request: The current HTTP request.

        Returns:
            A queryset with selected related fields for performance optimization.

        """
        return super().get_queryset(request).select_related("audience")
