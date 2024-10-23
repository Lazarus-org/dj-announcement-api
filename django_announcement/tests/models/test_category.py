import sys

import pytest

from django_announcement.models import AnnouncementCategory
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.models_category,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAnnouncementCategoryModel:
    """
    Test suite for the AnnouncementCategory model.
    """

    def test_str_method(self, announcement_category: AnnouncementCategory) -> None:
        """
        Test that the __str__ method returns the correct string representation of an announcement category.

        Asserts:
        -------
            - The string representation of the announcement category includes the name.
        """
        expected_str = announcement_category.name
        assert (
            str(announcement_category) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(announcement_category)}'."
