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
                    self.style.WARNING("To exclude certain apps or models:")
                )
                self.stdout.write(
                    "1. Modify the 'GENERATE_AUDIENCES_EXCLUDE_APPS' and 'GENERATE_AUDIENCES_EXCLUDE_APPS'"
                    " lists in the settings."
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

        for model in related_models:
            model_name = model._meta.verbose_name.title()
            audience, created = Audience.objects.get_or_create(
                name=model_name,
                defaults={"description": f"Auto-created audience for {model_name}"},
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created audience: {audience.name}")
                )

        self.stdout.write(self.style.SUCCESS("Finished creating audiences!"))

    @staticmethod
    def get_user_related_models() -> List:
        """Helper method to get models related to the user model."""
        user_related_models = []
        for model in apps.get_models():
            module_path = model.__module__
            app_label = model._meta.app_label
            model_name = model.__name__

            exclude_apps = config.generate_audiences_exclude_apps
            exclude_models = config.generate_audiences_exclude_models

            # Exclude specific apps or models provided
            if app_label in exclude_apps or model_name in exclude_models:
                continue
            # Ignore models from 'django' and 'django_announcement' app
            if module_path.startswith("django.") or module_path.startswith(
                "django_announcement."
            ):
                continue

            for field in model._meta.get_fields():
                if field.is_relation and field.related_model == UserModel:
                    user_related_models.append(model)
                    break
        return user_related_models
