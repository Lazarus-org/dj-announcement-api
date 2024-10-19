from typing import List

from django.core.management.base import BaseCommand
from django.apps import apps

from django_announcement.settings.conf import config
from django_announcement.utils.user_model import UserModel
from django_announcement.models import Audience


class Command(BaseCommand):
    help = "Dynamically create audiences based on models related to the User."

    def handle(self, *args, **kwargs):
        related_models = self.get_user_related_models()

        if not related_models:
            self.stdout.write(
                self.style.WARNING("No related models found to create audiences.")
            )
            return

        self.stdout.write(
            self.style.WARNING("The following related models were found:")
        )
        for i, model in enumerate(related_models, 1):
            self.stdout.write(f"{i}. {model}")

        while True:
            user_input = (
                input(
                    "\nAre these the correct target models? Type 'y' to proceed or 'n' to return"
                    " and modify the exclude list in settings: "
                )
                .strip()
                .lower()
            )

            if user_input == "n":
                self.stdout.write(
                    self.style.WARNING(
                        "To exclude certain apps or models, modify the settings:"
                    )
                )
                self.stdout.write(
                    "1. Adjust 'DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS' and"
                    " 'DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS'."
                )
                self.stdout.write(
                    "2. Re-run this command after adjusting the settings."
                )
                return
            elif user_input == "y":
                break
            else:
                self.stdout.write(
                    self.style.ERROR(
                        "Invalid input. Please type 'y' (Yes) or 'n' (No)."
                    )
                )

        # Fetch existing audiences for the related models in bulk
        model_names = [model._meta.verbose_name.title() for model in related_models]
        existing_audiences = Audience.objects.filter(name__in=model_names).values_list(
            "name", flat=True
        )

        audiences_to_create = []
        for model in related_models:
            model_name = model._meta.verbose_name.title()
            if model_name not in existing_audiences:
                audiences_to_create.append(
                    Audience(
                        name=model_name,
                        description=f"Auto-created audience for {model_name}",
                    )
                )

        # Bulk create the new audiences
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

        self.stdout.write(self.style.SUCCESS("Finished creating audiences!"))

    @staticmethod
    def get_user_related_models() -> List:
        """Helper method to get models related to the user model."""
        user_related_models = []

        exclude_apps = set(config.generate_audiences_exclude_apps)
        exclude_models = set(config.generate_audiences_exclude_models)

        for model in apps.get_models():
            module_path = model.__module__
            app_label = model._meta.app_label
            model_name = model.__name__

            # Exclude specific apps or models provided
            if app_label in exclude_apps or model_name in exclude_models:
                continue

            # Ignore models from 'django' and 'django_announcement' app
            if module_path.startswith("django.") or module_path.startswith(
                "django_announcement."
            ):
                continue

            # Check if the model has a relationship with the UserModel
            if any(
                field.is_relation and field.related_model == UserModel
                for field in model._meta.get_fields()
            ):
                user_related_models.append(model)

        return user_related_models
