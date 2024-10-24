import sys
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command

from django_announcement.management.commands.generate_audiences import (
    Command as GenerateAudiencesCommand,
)
from django_announcement.models import Audience
from django_announcement.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django_announcement.utils.user_model import UserModel

pytestmark = [
    pytest.mark.commands,
    pytest.mark.commands_generate_audiences,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestGenerateAudiencesCommand:
    """
    Test suite for the `generate_audiences` management command.
    """

    def create_mock_model(
        self,
        name: str,
        app_label: str,
        module_path: str,
        has_user_relation: bool = False,
    ):
        """
        Helper method to create a mock model object with the required `_meta` attributes.
        """
        mock_model = MagicMock()
        mock_model._meta.verbose_name = name
        mock_model._meta.app_label = app_label
        mock_model.__name__ = name
        mock_model.__module__ = module_path

        if has_user_relation:
            mock_field = MagicMock()
            mock_field.is_relation = True
            mock_field.related_model = UserModel
            mock_model._meta.get_fields.return_value = [mock_field]
        else:
            mock_model._meta.get_fields.return_value = []
        return mock_model

    @patch.object(GenerateAudiencesCommand, "get_user_related_models", return_value={})
    def test_no_related_models(self, mock_get_related_models: MagicMock) -> None:
        """
        Test that the command outputs the correct message when no related models are found.
        """
        out = StringIO()
        call_command("generate_audiences", stdout=out)
        assert "No related models found to create audiences." in out.getvalue()

    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    @patch("builtins.input", side_effect=["y"])
    def test_related_models_found(
        self, mock_input: MagicMock, mock_get_related_models: MagicMock
    ) -> None:
        """
        Test that the command correctly proceeds when related models are found and 'y' is entered.
        """
        mock_model = self.create_mock_model(
            "TestModel", "some_app", "some_module", has_user_relation=True
        )
        mock_get_related_models.return_value = {mock_model: "accessor_name"}

        out = StringIO()
        call_command("generate_audiences", stdout=out)

        assert "The following related models were found:" in out.getvalue()
        assert "Created audience: Testmodel" in out.getvalue()
        assert "Finished creating audiences!" in out.getvalue()

        # Assert that the audience was created
        assert Audience.objects.filter(name="Testmodel").exists()

    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    @patch("builtins.input", side_effect=["invalid", "y"])
    def test_invalid_input(
        self, mock_input: MagicMock, mock_get_related_models: MagicMock
    ) -> None:
        """
        Test that the command handles invalid user input and prompts again.
        """
        mock_model = self.create_mock_model(
            "TestModel", "some_app", "some_module", has_user_relation=True
        )
        mock_get_related_models.return_value = {mock_model: "accessor_name"}

        out = StringIO()
        call_command("generate_audiences", stdout=out)

        assert "Invalid input. Please type 'y' (Yes) or 'n' (No)." in out.getvalue()
        assert "Created audience: Testmodel" in out.getvalue()

        # Assert that the audience was created after valid input
        assert Audience.objects.filter(name="Testmodel").exists()

    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    @patch("builtins.input", side_effect=["y"])
    def test_audience_already_exists(
        self, mock_input: MagicMock, mock_get_related_models: MagicMock
    ) -> None:
        """
        Test that the command doesn't create a duplicate audience if it already exists.
        """
        # Create the audience beforehand
        Audience.objects.create(name="Testmodel", description="Existing audience")

        mock_model = self.create_mock_model(
            "TestModel", "some_app", "some_module", has_user_relation=True
        )
        mock_get_related_models.return_value = {mock_model: "accessor_name"}

        out = StringIO()
        call_command("generate_audiences", stdout=out)

        assert "Created audience: Testmodel" not in out.getvalue()
        assert "Finished creating audiences!" in out.getvalue()

        # Assert that no duplicate audience was created
        assert Audience.objects.filter(name="Testmodel").count() == 1

    @patch.object(UserModel._meta, "related_objects")
    def test_get_user_related_models(self, mock_related_objects: MagicMock) -> None:
        """
        Test the `get_user_related_models` method to ensure it correctly filters models based on settings and relations.
        """

        mock_related = MagicMock()
        mock_related.related_model = self.create_mock_model(
            "IncludedModel", "included_app", "some_module", has_user_relation=True
        )

        mock_related_objects.__iter__.return_value = [mock_related]

        # Calling the method
        command = GenerateAudiencesCommand()
        related_models = command.get_user_related_models()

        assert list(related_models.keys()) == [mock_related.related_model]

    @patch.object(GenerateAudiencesCommand, "get_user_related_models")
    @patch("builtins.input", side_effect=["n"])
    def test_user_declines_related_models(
        self, mock_input: MagicMock, mock_get_related_models: MagicMock
    ) -> None:
        """
        Test that the command correctly handles when the user declines the related models by typing 'n'.
        """
        mock_model = self.create_mock_model("TestModel", "included_app", "some_module")
        mock_get_related_models.return_value = {mock_model: "accessor_name"}

        out = StringIO()
        call_command("generate_audiences", stdout=out)

        assert "To exclude certain apps or models" in out.getvalue()
        assert "Re-run this command after adjusting the settings." in out.getvalue()
