from typing import Dict

import pytest
from django.utils.timezone import now, timedelta

from django_announcement.models import Announcement, AnnouncementCategory, Audience


@pytest.fixture
def setup_data() -> Dict[str, Announcement]:
    """
    Fixture to set up test data for announcements, categories, and audiences.

    Returns:
        Dict[str, Announcement]: A dictionary containing the created announcements and related data.
    """
    # Create mock audiences
    audience1: Audience = Audience.objects.create(name="Audience 1")
    audience2: Audience = Audience.objects.create(name="Audience 2")

    # Create mock categories
    category1: AnnouncementCategory = AnnouncementCategory.objects.create(
        name="Category 1"
    )
    category2: AnnouncementCategory = AnnouncementCategory.objects.create(
        name="Category 2"
    )

    # Create some announcements
    now_time = now()

    active_announcement: Announcement = Announcement.objects.create(
        title="Active Announcement",
        published_at=now_time - timedelta(days=1),  # Published yesterday
        expires_at=now_time + timedelta(days=1),  # Expires tomorrow
        category=category1,
    )
    active_announcement.audience.add(audience1)

    upcoming_announcement: Announcement = Announcement.objects.create(
        title="Upcoming Announcement",
        published_at=now_time + timedelta(days=1),  # Publishes tomorrow
        expires_at=now_time + timedelta(days=10),  # Expires in 10 days
        category=category2,
    )
    upcoming_announcement.audience.add(audience2)

    expired_announcement: Announcement = Announcement.objects.create(
        title="Expired Announcement",
        published_at=now_time - timedelta(days=10),  # Published 10 days ago
        expires_at=now_time - timedelta(days=1),  # Expired yesterday
        category=category1,
    )
    expired_announcement.audience.add(audience1)

    yield {
        "active": active_announcement,
        "upcoming": upcoming_announcement,
        "expired": expired_announcement,
        "audiences": [audience1, audience2],
        "categories": [category1, category2],
    }

    # Teardown: delete all created data
    Announcement.objects.all().delete()
    Audience.objects.all().delete()
    AnnouncementCategory.objects.all().delete()
