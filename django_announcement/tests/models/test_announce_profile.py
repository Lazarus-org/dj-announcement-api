import sys

import pytest

from django_announcement.models import UserAnnouncementProfile
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django_announcement.utils.user_model import get_username

pytestmark = [
    pytest.mark.models,
    pytest.mark.models_announcement_profile,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserAnnouncementProfileModel:
    """
    Test suite for the UserAnnouncementProfile model.
    """

    def test_str_method(
        self, user_announcement_profile: UserAnnouncementProfile
    ) -> None:
        """
        Test that the __str__ method returns the correct string representation of the user's announcement profile.

        Asserts:
        -------
            - The string representation of the profile includes the username.
        """
        expected_str = get_username(user_announcement_profile.user)
        assert (
            str(user_announcement_profile) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(user_announcement_profile)}'."
