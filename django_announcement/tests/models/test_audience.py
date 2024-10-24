import sys

import pytest

from django_announcement.models import Audience
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.models_audience,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAudienceModel:
    """
    Test suite for the Audience model.
    """

    def test_str_method(self, audience: Audience) -> None:
        """
        Test that the __str__ method returns the correct string representation of an audience.

        Asserts:
        -------
            - The string representation of the audience includes the name.
        """
        expected_str = audience.name
        assert (
            str(audience) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(audience)}'."
