import pytest
from django.contrib.admin import AdminSite
from django.http import HttpRequest

from django_announcement.admin import AnnouncementAdmin, UserAnnouncementProfileAdmin
from django_announcement.models import Announcement, UserAnnouncementProfile


@pytest.fixture
def announcement_admin() -> AnnouncementAdmin:
    """Fixture to create an instance of AnnouncementAdmin."""
    site = AdminSite()
    return AnnouncementAdmin(Announcement, site)


@pytest.fixture
def announce_profile_admin() -> UserAnnouncementProfileAdmin:
    """Fixture to create an instance of UserAnnouncementProfileAdmin."""
    site = AdminSite()
    return UserAnnouncementProfileAdmin(UserAnnouncementProfile, site)


@pytest.fixture
def mock_request() -> HttpRequest:
    """Fixture to mock an HttpRequest object."""
    return HttpRequest()
