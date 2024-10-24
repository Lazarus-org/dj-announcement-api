from typing import Dict, List, Tuple

from django.core.management.base import BaseCommand

from django_announcement.models import Audience
from django_announcement.settings.conf import config
from django_announcement.utils.user_model import UserModel


class Command(BaseCommand):
    """A Django management command to dynamically create audiences based on
    models related to the User model. It allows for filtering specific apps and
    models through configuration settings and includes optional user
    confirmation.

    Attributes:
    ----------
        EXCLUDE_APPS_SETTING: List of apps to exclude from the audience generation process.
        EXCLUDE_MODELS_SETTING: List of models to exclude from the audience generation process.

    """

    help = "Dynamically create audiences based on models related to the User."

    EXCLUDE_APPS_SETTING = config.generate_audiences_exclude_apps
    EXCLUDE_MODELS_SETTING = config.generate_audiences_exclude_models

    def add_arguments(self, parser):
        """Add optional arguments to the command parser.

        Args:
        ----
            parser: The argument parser instance to which the arguments are added.

        """
        parser.add_argument(
            "--skip-confirmation",
            action="store_true",
            help="Skip the confirmation prompt if no needed.",
        )

    def handle(self, *args: Tuple, **kwargs: Dict) -> None:
        """Main logic of the command. It retrieves user-related models,
        optionally prompts for confirmation, and creates new audiences if
        necessary.

        Args:
        ----
            *args: Additional positional arguments.
            **kwargs: Keyword arguments, such as 'skip-confirmation' to bypass user confirmation.

        """
        related_models = self.get_user_related_models()
        related_model_keys = list(related_models.keys())

        if not related_models:
            self.stdout.write(
                self.style.WARNING("No related models found to create audiences.")
            )
            return

        self._print_related_models(related_model_keys)

        if not kwargs.get("skip_confirmation") and not self._confirm_proceed():
            self._print_exclude_instructions()
            return

        self._create_audiences(related_model_keys)

        self.stdout.write(self.style.SUCCESS("Finished creating audiences!"))

    @staticmethod
    def get_user_related_models() -> Dict:
        """Fetch user-related models, excluding apps and models defined in the
        settings.

        Returns:
        -------
            Dict: A dictionary of related models, excluding those specified in settings.

        """
        exclude_apps = set(Command.EXCLUDE_APPS_SETTING)
        exclude_models = set(Command.EXCLUDE_MODELS_SETTING)

        return {
            rel.related_model: rel.get_accessor_name()
            for rel in UserModel._meta.related_objects
            if (
                rel.related_model._meta.app_label not in exclude_apps
                and rel.related_model.__name__ not in exclude_models
                and not rel.related_model.__module__.startswith(
                    ("django.", "django_announcement.")
                )
            )
        }

    def _print_related_models(self, related_models: List) -> None:
        """Print the list of related models for the user to review.

        Args:
        ----
            related_models (List): A list of related models to be displayed.

        """
        self.stdout.write(
            self.style.WARNING("The following related models were found:")
        )
        for i, model in enumerate(related_models, 1):
            self.stdout.write(f"{i}. {model}")

    def _confirm_proceed(self) -> bool:
        """Prompt the user for confirmation to proceed with the audience
        creation.

        Returns:
        -------
            bool: True if the user confirms, False otherwise.

        """
        while True:
            user_input = (
                input(
                    "\nAre these the correct target models? Type 'y' to proceed or 'n' to modify settings: "
                )
                .strip()
                .lower()
            )

            if user_input == "n":
                return False
            elif user_input == "y":
                return True
            else:
                self.stdout.write(
                    self.style.ERROR(
                        "Invalid input. Please type 'y' (Yes) or 'n' (No)."
                    )
                )

    def _print_exclude_instructions(self) -> None:
        """Print instructions to modify exclude settings."""
        self.stdout.write(
            self.style.WARNING(
                "To exclude certain apps or models, modify the settings:"
            )
        )
        self.stdout.write(
            "1. Adjust 'DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS'"
        )
        self.stdout.write(
            "2. Adjust 'DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS'"
        )
        self.stdout.write("3. Re-run this command after adjusting the settings.")

    def _create_audiences(self, related_models_list: List) -> None:
        """Create audiences based on the related models if they do not already
        exist.

        Args:
        ----
            related_models_list (List): A list of related models for which to create audiences.

        """
        model_names = [
            model._meta.verbose_name.title() for model in related_models_list
        ]
        existing_audiences = set(
            Audience.objects.filter(name__in=model_names).values_list("name", flat=True)
        )

        audiences_to_create = [
            Audience(
                name=model_name, description=f"Auto-created audience for {model_name}"
            )
            for model_name in model_names
            if model_name not in existing_audiences
        ]

        if audiences_to_create:
            Audience.objects.bulk_create(audiences_to_create)
            for audience in audiences_to_create:
                self.stdout.write(
                    self.style.SUCCESS(f"Created audience: {audience.name}")
                )
        else:
            self.stdout.write(
                self.style.WARNING("No new audiences needed to be created.")
            )
