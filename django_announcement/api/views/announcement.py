from typing import List, Type

from django.db.models import QuerySet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from django_announcement.api.serializers.announcement import (
    AnnouncementSerializer,
    SimpleAnnouncementSerializer,
)
from django_announcement.mixins.config_api_attrs import ConfigureAttrsMixin
from django_announcement.mixins.control_api_methods import ControlAPIMethodsMixin
from django_announcement.models.announcement import Announcement
from django_announcement.settings.conf import config

try:
    from django_filters.rest_framework import DjangoFilterBackend

    django_filter_installed = True
except ImportError:  # pragma: no cover
    django_filter_installed = False


class AnnouncementViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    ControlAPIMethodsMixin,
    ConfigureAttrsMixin,
):
    """API ViewSet for managing announcements.

    Provides list and retrieve operations for announcements, dynamically adjusting
    the level of announcement detail based on the user's role or system configuration.

    Features:
    - List Announcements: Retrieves a list of available announcements.
    - Retrieve Announcement: Fetch detailed information about a specific announcement by its ID.

    Customizations:
    - Dynamic Serializer: Depending on the user's role or configuration, selects between
      `AnnouncementSerializer` for detailed information and `SimpleAnnouncementSerializer` for basic announcement data.
    - Filtering and Searching: Supports filtering, searching, and ordering through Django filters
      (`DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`) if `django-filter` is installed

    Methods:
    - `GET /announcements/`: List announcements.
    - `GET /announcements/<id>/`: Retrieve detailed information about a specific announcement.

    Permissions:
    - Only authenticated users with proper permissions can interact with announcements.

    """

    filter_backends: List = [
        *([DjangoFilterBackend] if django_filter_installed else []),
        OrderingFilter,
        SearchFilter,
    ]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the viewset and configure attributes based on settings.

        Disables the 'list' and 'retrieve' methods if their corresponding settings
        (`api_allow_list` and `api_allow_retrieve`) are set to `False`.

        """
        super().__init__(*args, **kwargs)
        self.configure_attrs()

        # Check the setting to enable or disable the list method
        if not config.api_allow_list:
            self.disable_methods(["LIST"])

        # Check the setting to enable or disable the retrieve method
        if not config.api_allow_retrieve:
            self.disable_methods(["RETRIEVE"])

    def get_serializer_class(self) -> Type[Serializer]:
        """Get the appropriate serializer class based on the user's role and
        configuration.

        Returns:
            Type[Serializer]: The serializer class to use for the current request.

        """
        if self.request.user.is_staff or config.include_serializer_full_details:
            return AnnouncementSerializer

        return SimpleAnnouncementSerializer

    def get_staff_queryset(self) -> QuerySet:
        """Get the queryset for staff users. Staff users can view all
        announcements with full details.

        Returns:
            QuerySet: A queryset all announcements for staff users.

        """
        return Announcement.objects.all()

    def get_queryset(self) -> QuerySet:
        """Get the queryset of available announcements based on user's
        audiences.

        Returns:
            QuerySet: A queryset of announcements suitable for the current user.

        """
        if self.request.user.is_staff:
            return self.get_staff_queryset()

        user_audiences = self.request.user.announcement_profile.audiences.values_list(
            "id", flat=True
        )
        return Announcement.objects.active().get_by_audience(user_audiences)
