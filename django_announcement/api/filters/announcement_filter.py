from django.apps import apps
from django_filters import BooleanFilter
from django_filters.rest_framework import DateTimeFromToRangeFilter, FilterSet


class AnnouncementFilter(FilterSet):
    """Filter set for filtering announcements based on various criteria."""

    created_at = DateTimeFromToRangeFilter(
        field_name="created_at",
        lookup_expr="range",
        help_text="Filter announcements by created_at within a specific range.",
    )

    published_at = DateTimeFromToRangeFilter(
        field_name="published_at",
        lookup_expr="range",
        help_text="Filter announcements by published_at within a specific range.",
    )

    expires_at = DateTimeFromToRangeFilter(
        field_name="expires_at",
        lookup_expr="range",
        help_text="Filter announcements by expires_at within a specific range.",
    )

    not_expired = BooleanFilter(
        field_name="expires_at",
        method="filter_not_expired",
        label="active (not expired)",
        help_text="Filter announcements that have not yet expired.",
    )

    class Meta:
        model = None
        fields = {
            "audience__id": ["exact"],
            "category__id": ["exact"],
            "title": [
                "icontains",
                "exact",
            ],
            "content": ["icontains"],
        }

    def filter_not_expired(self, queryset, name, value):
        """Filter announcements that are not expired (i.e., expires_at is None
        or in the future)."""
        from django_announcement.models.announcement import Announcement

        self.Meta.model = Announcement
        return queryset.active() if value else queryset
