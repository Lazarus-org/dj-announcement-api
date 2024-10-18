from django.core.management.base import BaseCommand
from django_announcement.utils.user_model import UserModel
from django.db import transaction
from django.db.models import Q
from django_announcement.models import Audience, UserAnnouncementProfile
from django_announcement.management.commands.generate_audiences import Command as cmd


class Command(BaseCommand):
    help = "Assign users to the dynamically created audiences using UserAnnouncementProfile model."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        user_related_models = cmd.get_user_related_models()

        if not Audience.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    "No audiences found. Please run the 'generate_audiences' command first."
                )
            )
            return

        user_filter = Q()
        audiences_mapping = {}

        for model in user_related_models:
            user_filter |= Q(**{f"{model._meta.model_name}__isnull": False})

            audience_name = model._meta.verbose_name.title()
            try:
                audience = Audience.objects.get(name=audience_name)
                audiences_mapping[model] = audience
            except Audience.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Audience '{audience_name}' does not exist, skipping."
                    )
                )

        related_users = UserModel.objects.filter(user_filter).distinct()

        if not related_users:
            self.stdout.write(
                self.style.WARNING("No users found related to the provided models.")
            )
            return

        existing_profiles = UserAnnouncementProfile.objects.filter(
            user__in=related_users
        ).values_list("user_id", flat=True)

        users_without_profiles = related_users.exclude(id__in=existing_profiles)

        # Bulk create profiles for users without profiles
        user_profiles_to_create = [
            UserAnnouncementProfile(user=user) for user in users_without_profiles
        ]
        UserAnnouncementProfile.objects.bulk_create(user_profiles_to_create)

        # Fetch all profiles to update their audiences
        user_profiles = UserAnnouncementProfile.objects.filter(user__in=related_users)

        # Assign audiences to profiles
        for model, audience in audiences_mapping.items():
            related_users_for_model = related_users.filter(
                **{f"{model._meta.model_name}__isnull": False}
            )
            profiles_for_model = user_profiles.filter(user__in=related_users_for_model)

            for profile in profiles_for_model:
                profile.audiences.add(audience)

        self.stdout.write(
            self.style.SUCCESS(
                "All users have been assigned to audiences successfully."
            )
        )
