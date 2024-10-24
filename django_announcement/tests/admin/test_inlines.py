import sys
from unittest.mock import Mock

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import User

from django_announcement.admin.inlines import AudienceInline
from django_announcement.models import Announcement, Audience, AudienceAnnouncement
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.admin_inlines,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAudienceInline:
    """Tests for the AudienceInline admin class."""

    def test_get_queryset(
        self, admin_user: User, audience: Audience, announcement: Announcement
    ) -> None:
        """
        Test the get_queryset method of AudienceInline.

        This test verifies that the get_queryset method correctly returns a queryset
        that includes the relevant AudienceAnnouncement instances associated with the
        given Audience and Announcement. It ensures that the method properly filters
        the queryset based on the user context.

        Args:
        ----
            admin_user (User ): The admin user performing the action.
            audience (Audience): The audience instance to be associated with the announcement.
            announcement (Announcement): The announcement instance linked to the audience.
        """
        audience_inline = AudienceInline(
            parent_model=AudienceAnnouncement, admin_site=site
        )

        audience_announcement, created = AudienceAnnouncement.objects.get_or_create(
            announcement=announcement, audience=audience
        )

        request = Mock()
        request.user = admin_user

        queryset = audience_inline.get_queryset(request)

        # Check that the queryset contains the expected audience announcement
        assert audience_announcement in queryset
