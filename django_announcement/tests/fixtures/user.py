import pytest
from django.contrib.auth.models import User

from django_announcement.models import Audience, UserAnnouncementProfile


@pytest.fixture
def user(db, audience: Audience) -> User:
    """
    Fixture to create a standard User instance for testing.

    Args:
        db: The database fixture to set up the test database.
        audience (Audience): the Audience fixture to set up profile

    Returns:
        User: The created User instance with username "testuser".
    """
    user = User.objects.create_user(
        username="testuser", password="12345", email="testuser@example.com"
    )
    profile = UserAnnouncementProfile.objects.create(user=user)
    profile.audiences.add(audience)
    return user


@pytest.fixture
def admin_user(db) -> User:
    """
    Fixture to create a superuser with admin access for testing.

    Args:
        db: The database fixture to set up the test database.

    Returns:
        User: The created superuser with username "admin".
    """
    return User.objects.create_superuser(username="admin", password="password")
