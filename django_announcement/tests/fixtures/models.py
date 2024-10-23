import pytest

from django_announcement.models import (
    Announcement,
    AnnouncementCategory,
    Audience,
    UserAnnouncementProfile,
)
from django_announcement.utils.user_model import UserModel


@pytest.fixture
def announcement_category() -> AnnouncementCategory:
    """
    Fixture to create an AnnouncementCategory instance.
    """
    return AnnouncementCategory.objects.create(name="General")


@pytest.fixture
def announcement(
    announcement_category: AnnouncementCategory, audience: Audience
) -> Announcement:
    """
    Fixture to create an Announcement instance.
    """
    announcement = Announcement.objects.create(
        title="Test Announcement",
        content="This is a test announcement.",
        category=announcement_category,
    )
    announcement.audience.add(audience)
    return announcement


@pytest.fixture
def audience(db) -> Audience:
    """
    Fixture to create an Audience instance.
    """
    return Audience.objects.create(
        name="VIP",
        description="A group of VIP users for exclusive announcements.",
    )


@pytest.fixture
def user_announcement_profile(audience: Audience) -> UserAnnouncementProfile:
    """
    Fixture to create a UserAnnouncementProfile instance.
    """
    test_user = UserModel.objects.create_user(
        username="testuser", password="password123"
    )
    profile = UserAnnouncementProfile.objects.create(user=test_user)
    profile.audiences.add(audience)
    return profile
