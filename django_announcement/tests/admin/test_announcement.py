import sys
from unittest.mock import MagicMock

import pytest
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db.models import ForeignKey
from django.http import HttpRequest
from django.test import Client, RequestFactory
from django.urls import reverse

from django_announcement.admin import AnnouncementAdmin
from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django_announcement.utils.user_model import UserModel

pytestmark = [
    pytest.mark.admin,
    pytest.mark.admin_announcement,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAnnouncementAdmin:
    """Tests for the AnnouncementAdmin class."""

    def test_list_view(self, admin_user: UserModel, client: Client) -> None:
        """
        Test the list view of the AnnouncementAdmin.

        This test checks that the list view is accessible to an admin user
        and returns a status code of 200 OK.

        Args:
        ----
            admin_user (User Model): The admin user for authentication.
            client (Client): The Django test client used to simulate requests.
        """
        client.login(username="admin", password="password")
        url = reverse("admin:django_announcement_announcement_changelist")
        response = client.get(url)

        assert response.status_code == 200, "Expected the status code to be 200 OK."

    def test_get_queryset(
        self,
        announcement_admin: AnnouncementAdmin,
        admin_user: UserModel,
        rf: RequestFactory,
    ) -> None:
        """
        Test that get_queryset optimizes performance by selecting related fields.

        This test ensures that the queryset returned by the get_queryset method
        includes the 'category' field in its select_related call, which is important
        for performance optimization.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
            admin_user (User Model): The admin user for authentication.
            rf (RequestFactory): A factory for creating request objects.
        """
        request = rf.get("/admin/")
        request.user = admin_user
        queryset = announcement_admin.get_queryset(request)

        assert (
            "category" in queryset.query.select_related
        ), "Expected 'category' to be in select_related."

    def test_autocomplete_fields(self, announcement_admin: AnnouncementAdmin) -> None:
        """
        Test that 'category' is in the autocomplete fields.

        This test checks that the 'category' field is included in the
        autocomplete_fields of the AnnouncementAdmin.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
        """
        assert (
            "category" in announcement_admin.autocomplete_fields
        ), "Expected 'category' in autocomplete_fields."

    def test_list_display(self, announcement_admin: AnnouncementAdmin) -> None:
        """
        Test that list_display includes correct fields.

        This test verifies that the list_display attribute of the AnnouncementAdmin
        includes the expected fields, ensuring that the admin interface displays
        the correct information.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
        """
        expected_display = BaseModelAdmin.list_display + [
            "title",
            "category",
            "created_at",
            "expires_at",
        ]
        assert (
            announcement_admin.list_display == expected_display
        ), "list_display fields mismatch."

    def test_search_fields(self, announcement_admin: AnnouncementAdmin) -> None:
        """
        Test that search_fields include correct fields.

        This test checks that the search_fields attribute of the AnnouncementAdmin
        includes the expected fields, allowing users to search effectively.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
        """
        expected_search_fields = BaseModelAdmin.search_fields + [
            "title",
            "content",
            "audience__name",
        ]
        assert (
            announcement_admin.search_fields == expected_search_fields
        ), "search_fields fields mismatch."

    def test_fieldsets(self, announcement_admin: AnnouncementAdmin) -> None:
        """
        Test that the fieldsets include the expected fields.

        This test ensures that the fieldsets attribute of the AnnouncementAdmin
        is correctly defined, including all necessary fields and descriptions.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
        """
        expected_fieldsets = [
            (
                None,
                {
                    "fields": ("title", "content", "category", "attachment"),
                    "description": "Primary fields related to the announcement,"
                    " including the title, content, category and attachment.",
                },
            ),
            (
                "Additional Information",
                {
                    "fields": ("published_at", "expires_at"),
                    "description": "Details regarding the announcement's publish and expiration date.",
                },
            ),
        ] + BaseModelAdmin.fieldsets
        assert announcement_admin.fieldsets == expected_fieldsets, "fieldsets mismatch."

    @pytest.mark.django_db
    def test_formfield_for_foreignkey_overrides_widget(
        self, announcement_admin: AnnouncementAdmin, mock_request: HttpRequest
    ) -> None:
        """
        Test that AnnouncementAdmin correctly overrides the form field widget for foreign keys
        to use ForeignKeyRawIdWidget.

        This test ensures that when a foreign key field is rendered, it uses the
        ForeignKeyRawIdWidget, allowing for a better user experience in the admin interface.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
            mock_request (HttpRequest): A mock HTTP request object.
        """
        # Create a mock for ForeignKey field
        mock_db_field = MagicMock(spec=ForeignKey)

        # Mock the remote_field and model attributes properly
        mock_db_field.remote_field = MagicMock()
        mock_model = MagicMock()
        mock_model.__name__ = "MockModel"
        mock_db_field.remote_field.model = mock_model

        # Mock the formfield method on the ForeignKey field
        mock_db_field.formfield = MagicMock(return_value="formfield_response")

        result = announcement_admin.formfield_for_foreignkey(
            mock_db_field, mock_request
        )

        kwargs = mock_db_field.formfield.call_args[1]

        # Assert that the widget is an instance of ForeignKeyRawIdWidget
        assert isinstance(kwargs["widget"], ForeignKeyRawIdWidget)

        # Assert that the method returns the expected formfield result
        assert result == "formfield_response"

    def test_formfield_for_foreignkey_sets_default_queryset(
        self, announcement_admin: AnnouncementAdmin, mock_request: HttpRequest
    ) -> None:
        """
        Test that the form field for foreign keys in AnnouncementAdmin has the default queryset
        set correctly if not provided.

        This test checks that when no custom queryset is provided, the form field for
        foreign keys correctly uses the default queryset from get_field_queryset.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
            mock_request (HttpRequest): A mock HTTP request object.
        """
        # Mock db_field with a ForeignKey field
        mock_db_field = MagicMock(spec=ForeignKey)
        mock_db_field.remote_field = MagicMock()
        mock_db_field.formfield = MagicMock(return_value="formfield_response")

        # Mock get_field_queryset method
        mock_queryset = MagicMock()
        announcement_admin.get_field_queryset = MagicMock(return_value=mock_queryset)

        # Call formfield_for_foreignkey to get the modified form field
        result = announcement_admin.formfield_for_foreignkey(
            mock_db_field, mock_request
        )

        # Ensure the queryset is set correctly
        mock_db_field.formfield.assert_called_once()
        kwargs = mock_db_field.formfield.call_args[1]
        assert kwargs["queryset"] == mock_queryset

        # Assert that the method returns the expected formfield result
        assert result == "formfield_response"

    @pytest.mark.django_db
    def test_formfield_for_foreignkey_custom_queryset(
        self, announcement_admin: AnnouncementAdmin, mock_request: HttpRequest
    ) -> None:
        """
        Test that a custom queryset passed in kwargs to AnnouncementAdmin is respected and not overridden.

        This test ensures that when a custom queryset is provided, it is used
        instead of the default queryset, allowing for more flexible data handling.

        Args:
        ----
            announcement_admin (AnnouncementAdmin): The admin class being tested.
            mock_request (HttpRequest): A mock HTTP request object.
        """
        # Mock db_field with a ForeignKey field
        mock_db_field = MagicMock(spec=ForeignKey)

        # Mock the remote_field and model attributes properly
        mock_db_field.remote_field = MagicMock()
        mock_model = MagicMock()
        mock_model.__name__ = "MockModel"
        mock_db_field.remote_field.model = mock_model

        # Mock the formfield method on the ForeignKey field
        mock_db_field.formfield = MagicMock(return_value="formfield_response")

        custom_queryset = MagicMock()

        result = announcement_admin.formfield_for_foreignkey(
            mock_db_field, mock_request, queryset=custom_queryset
        )

        # Ensure the custom queryset is respected
        mock_db_field.formfield.assert_called_once()
        kwargs = mock_db_field.formfield.call_args[1]
        assert kwargs["queryset"] == custom_queryset

        # Assert that the method returns the expected formfield result
        assert result == "formfield_response"
