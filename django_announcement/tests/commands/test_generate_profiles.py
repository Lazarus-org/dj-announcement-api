import sys
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command

from django_announcement.management.commands.generate_audiences import (
    Command as GenerateAudiencesCommand,
)
from django_announcement.models import Audience, UserAnnouncementProfile, UserAudience
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django_announcement.utils.user_model import UserModel

pytestmark = [
    pytest.mark.commands,
    pytest.mark.commands_generate_profiles,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestGenerateProfilesCommand:
    """
    Test suite for the `generate_profiles` management command.
    """

    @patch("builtins.input", side_effect=["no"])
    def test_profiles_not_run_if_audiences_not_generated(self, mock_input: MagicMock):
        """
        Test that the command exits if 'generate_audiences' has not been run.
        """
        out = StringIO()
        call_command("generate_profiles", stdout=out)
        assert "Exiting... Please run 'generate_audiences' first." in out.getvalue()

    @patch("builtins.input", side_effect=["yes"])
    @patch.object(
        GenerateAudiencesCommand,
        "get_user_related_models",
        side_effect=Exception("Simulated exception"),
    )
    def test_get_user_related_models_exception(
        self, mock_get_related_models: MagicMock, mock_input: MagicMock
    ):
        """
        Test that the command exits if an exception is raised when fetching user-related models.
        """
        out = StringIO()

        # Call the management command, expecting it to handle the exception internally
        call_command("generate_profiles", stdout=out)

        # Assert that the appropriate error message is in the output
        assert (
            "Error fetching user-related models: Simulated exception" in out.getvalue()
        )

    @patch("builtins.input", side_effect=["yes"])
    @patch.object(GenerateAudiencesCommand, "get_user_related_models", return_value={})
    def test_no_related_models(
        self,
        mock_get_related_models: MagicMock,
        mock_input: MagicMock,
        audience: Audience,
    ):
        """
        Test that the command outputs a message when no related models are found.
        """
        out = StringIO()
        call_command("generate_profiles", stdout=out)
        assert "No users found related to the provided models." in out.getvalue()

    @patch("builtins.input", side_effect=["yes"])
    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    def test_no_audiences_found(
        self, mock_get_related_models: MagicMock, mock_input: MagicMock, user: UserModel
    ):
        """
        Test that the command exits if no audiences are found.
        """
        Audience.objects.all().delete()

        mock_get_related_models.return_value = {
            UserAnnouncementProfile: "announcement_profile"
        }

        out = StringIO()
        call_command("generate_profiles", stdout=out)

        assert (
            "No valid audiences found, Please run 'generate_audiences' first. Exiting..."
            in out.getvalue()
        )

    @patch("builtins.input", side_effect=["yes"])
    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    @patch("django_announcement.management.commands.generate_profiles.Audience.objects")
    @patch(
        "django_announcement.management.commands.generate_profiles.UserAnnouncementProfile.objects"
    )
    def test_profiles_created_for_related_users(
        self,
        mock_user_profile_queryset: MagicMock,
        mock_audience_queryset: MagicMock,
        mock_get_related_models: MagicMock,
        mock_input: MagicMock,
        user,
    ):
        """
        Test that the command creates profiles correctly for related users.
        """
        # Mocking the related model and audience
        mock_get_related_models.return_value = {
            UserAnnouncementProfile: "announcement_profile"
        }

        mock_audience = Audience(name="User Announcement Profile")
        mock_audience_queryset.exists.return_value = True
        mock_audience_queryset.filter.return_value = [mock_audience]

        # Call the management command
        out = StringIO()
        call_command("generate_profiles", stdout=out)

        # Assert that profiles were created and audiences were assigned
        assert (
            "All users have been assigned to existing audiences successfully."
            in out.getvalue()
        )

        # Check if bulk_create was called for both UserAnnouncementProfile and UserAudience
        assert mock_user_profile_queryset.bulk_create.called

    @patch("builtins.input", side_effect=["yes"])
    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    def test_audiences_created_for_related_users(
        self, mock_get_related_models: MagicMock, mock_input: MagicMock, user: UserModel
    ):
        """
        Test that the command creates profiles and assigns audiences correctly for related users.
        """
        # Mocking the related model and audience
        mock_get_related_models.return_value = {
            UserAnnouncementProfile: "announcement_profile"
        }

        Audience.objects.create(name="User Announcement Profile")

        # Clear the necessary table
        UserAudience.objects.all().delete()

        # Call the management command
        out = StringIO()
        call_command("generate_profiles", stdout=out)

        # Assert that profiles were created and audiences were assigned
        assert (
            "All users have been assigned to existing audiences successfully."
            in out.getvalue()
        )

        # Assert that UserAnnouncementProfile successfully created for the target user
        user_announce_profile = UserAnnouncementProfile.objects.filter(user=user)[0]
        assert user_announce_profile

        #  Assert that audience successfully assigned to the target user
        assert UserAudience.objects.filter(user_announce_profile=user_announce_profile)
