import sys

import pytest

from django_announcement.models import Announcement
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.models_announcement,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAnnouncementModel:
    """
    Test suite for the Announcement model.
    """

    def test_str_method(self, announcement: Announcement) -> None:
        """
        Test that the __str__ method returns the correct string representation of an announcement.

        Asserts:
        -------
            - The string representation of the announcement includes the title.
        """
        expected_str = announcement.title
        assert (
            str(announcement) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(announcement)}'."
