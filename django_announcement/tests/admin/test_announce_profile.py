import sys

import pytest
from django.db.models import QuerySet
from django.test import Client, RequestFactory
from django.urls import reverse

from django_announcement.admin import UserAnnouncementProfileAdmin
from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models import UserAnnouncementProfile
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django_announcement.utils.user_model import USERNAME_FIELD, UserModel

pytestmark = [
    pytest.mark.admin,
    pytest.mark.admin_announcement_profile,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserAnnouncementProfileAdmin:
    """
    Test suite for the `UserAnnouncementProfileAdmin` class.

    This test class verifies the behavior and functionality of the
    `UserAnnouncementProfileAdmin` in managing user announcement profiles.
    """

    def test_list_view(self, admin_user: UserModel, client: Client) -> None:
        """
        Test the list view of the `UserAnnouncementProfileAdmin`.

        This test ensures that the list view loads correctly with a
        status code of 200 OK.

        Args:
        ----
            admin_user (UserModel): The admin user for authentication.
            client (Client): The Django test client.
        """
        client.login(username="admin", password="password")
        url = reverse("admin:django_announcement_userannouncementprofile_changelist")
        response = client.get(url)

        assert response.status_code == 200, "Expected status code 200 OK."

    def test_get_queryset(
        self,
        announce_profile_admin: UserAnnouncementProfileAdmin,
        admin_user: UserModel,
        rf: RequestFactory,
    ) -> None:
        """
        Test that the `get_queryset` method optimizes performance by selecting related fields.

        This test checks whether `select_related` is used for the 'user' field
        to optimize database queries.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
            admin_user (UserModel): The admin user initiating the request.
            rf (RequestFactory): The request factory for generating requests.
        """
        request = rf.get("/admin/")
        request.user = admin_user
        queryset: QuerySet = announce_profile_admin.get_queryset(request)

        assert (
            "user" in queryset.query.select_related
        ), "Expected 'user' to be in select_related."

    def test_get_username(
        self,
        announce_profile_admin: UserAnnouncementProfileAdmin,
        user_announcement_profile: UserAnnouncementProfile,
    ) -> None:
        """
        Test that `get_username` correctly retrieves the username for a `UserAnnouncementProfile`.

        This test ensures that the `get_username` method returns the username associated
        with the user announcement profile.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
            user_announcement_profile (UserAnnouncementProfile): The profile for which the username is fetched.
        """
        username: str = announce_profile_admin.get_username(user_announcement_profile)
        assert (
            username == user_announcement_profile.user.username
        ), "Expected correct username to be returned."

    def test_autocomplete_fields(
        self, announce_profile_admin: UserAnnouncementProfileAdmin
    ) -> None:
        """
        Test that 'user' and 'audiences' are included in the autocomplete fields.

        This test verifies that the fields 'user' and 'audiences' are set for
        autocompletion in the admin interface.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
        """
        expected_fields = ["user", "audiences"]
        assert (
            announce_profile_admin.autocomplete_fields == expected_fields
        ), "Expected 'user' and 'audiences' in autocomplete_fields."

    def test_list_display(
        self, announce_profile_admin: UserAnnouncementProfileAdmin
    ) -> None:
        """
        Test that `list_display` includes the correct fields.

        This test checks that `list_display` includes fields such as
        'get_username', 'created_at', and 'updated_at' in addition to
        the fields inherited from `BaseModelAdmin`.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
        """
        expected_display = BaseModelAdmin.list_display + [
            "get_username",
            "created_at",
            "updated_at",
        ]
        assert (
            announce_profile_admin.list_display == expected_display
        ), "list_display fields mismatch."

    def test_search_fields(
        self, announce_profile_admin: UserAnnouncementProfileAdmin
    ) -> None:
        """
        Test that `search_fields` include the correct fields.

        This test ensures that `search_fields` includes fields like 'user__username',
        'user__id', and 'audiences__name' along with those inherited from `BaseModelAdmin`.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
        """
        expected_search_fields = BaseModelAdmin.search_fields + [
            f"user__{USERNAME_FIELD}",
            "user__id",
            "audiences__name",
        ]
        assert (
            announce_profile_admin.search_fields == expected_search_fields
        ), "search_fields fields mismatch."

    def test_fieldsets(
        self, announce_profile_admin: UserAnnouncementProfileAdmin
    ) -> None:
        """
        Test that the `fieldsets` include the expected fields.

        This test checks that `fieldsets` contains the correct grouping of fields,
        specifically ensuring that the 'user' field is included along with those
        inherited from `BaseModelAdmin`.

        Args:
        ----
            announce_profile_admin (UserAnnouncementProfileAdmin): The admin class being tested.
        """
        expected_fieldsets = [
            (None, {"fields": ("user",)}),
        ] + BaseModelAdmin.fieldsets
        assert (
            announce_profile_admin.fieldsets == expected_fieldsets
        ), "fieldsets mismatch."
