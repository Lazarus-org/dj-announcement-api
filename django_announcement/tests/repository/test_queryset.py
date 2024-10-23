import sys
from typing import Dict

import pytest
from django.db.models import QuerySet

from django_announcement.models import Announcement
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.queryset,
    pytest.mark.queryset_announcement,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAnnouncementQuerySet:
    """
    Test suite for AnnouncementQuerySet class and its methods.
    """

    def test_active_announcements(self, setup_data: Dict[str, Announcement]) -> None:
        """
        Test the active() method to ensure it returns currently active announcements.

        Args:
        ----
            setup_data (Dict[str, Announcement]): The fixture data for announcements.
        """
        active_announcements: QuerySet = Announcement.objects.active()

        assert setup_data["active"] in active_announcements
        assert setup_data["upcoming"] not in active_announcements
        assert setup_data["expired"] not in active_announcements

    def test_upcoming_announcements(self, setup_data: Dict[str, Announcement]) -> None:
        """
        Test the upcoming() method to ensure it returns announcements scheduled for the future.

        Args:
        ----
            setup_data (Dict[str, Announcement]): The fixture data for announcements.
        """
        upcoming_announcements: QuerySet = Announcement.objects.upcoming()

        assert setup_data["upcoming"] in upcoming_announcements
        assert setup_data["active"] not in upcoming_announcements
        assert setup_data["expired"] not in upcoming_announcements

    def test_expired_announcements(self, setup_data: Dict[str, Announcement]) -> None:
        """
        Test the expired() method to ensure it returns announcements that have expired.

        Args:
        ----
            setup_data (Dict[str, Announcement]): The fixture data for announcements.
        """
        expired_announcements: QuerySet = Announcement.objects.expired()

        assert setup_data["expired"] in expired_announcements
        assert setup_data["active"] not in expired_announcements
        assert setup_data["upcoming"] not in expired_announcements

    def test_get_by_audience(self, setup_data: Dict[str, Announcement]) -> None:
        """
        Test the get_by_audience() method to ensure it filters by audience correctly.

        Args:
        ----
            setup_data (Dict[str, Announcement]): The fixture data for announcements.
        """
        audience1_announcements: QuerySet = Announcement.objects.get_by_audience(
            setup_data["audiences"][0]
        )

        assert setup_data["active"] in audience1_announcements
        assert setup_data["expired"] in audience1_announcements
        assert setup_data["upcoming"] not in audience1_announcements

        audience2_announcements: QuerySet = Announcement.objects.get_by_audience(
            setup_data["audiences"][1]
        )

        assert setup_data["upcoming"] in audience2_announcements
        assert setup_data["active"] not in audience2_announcements
        assert setup_data["expired"] not in audience2_announcements

    def test_get_by_category(self, setup_data: Dict[str, Announcement]) -> None:
        """
        Test the get_by_category() method to ensure it filters by category correctly.

        Args:
        ----
            setup_data (Dict[str, Announcement]): The fixture data for announcements.
        """
        category1_announcements: QuerySet = Announcement.objects.get_by_category(
            setup_data["categories"][0]
        )

        assert setup_data["active"] in category1_announcements
        assert setup_data["expired"] in category1_announcements
        assert setup_data["upcoming"] not in category1_announcements

        category2_announcements: QuerySet = Announcement.objects.get_by_category(
            setup_data["categories"][1]
        )

        assert setup_data["upcoming"] in category2_announcements
        assert setup_data["active"] not in category2_announcements
        assert setup_data["expired"] not in category2_announcements
