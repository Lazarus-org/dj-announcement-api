import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Fixture to provide an API client for making requests to the viewset.
    """
    return APIClient()
