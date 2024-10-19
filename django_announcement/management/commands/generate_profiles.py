import sys
from django.core.management.base import BaseCommand
from django_announcement.utils.user_model import UserModel
from django.db import transaction
from django.db.models import Q
from django_announcement.models import Audience, UserAnnouncementProfile, UserAudience
from django_announcement.management.commands.generate_audiences import Command as cmd


class Command(BaseCommand):
    help = "Assign users to the dynamically created audiences using UserAnnouncementProfile model."

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                "Ensure you've run the 'generate_audiences' command before proceeding."
            )
        )
        proceed = (
            input("Have you already run 'generate_audiences'? (yes/no): ")
            .strip()
            .lower()
        )

        if proceed not in ("yes", "y"):
            self.stdout.write(
                self.style.SUCCESS("Exiting... Please run 'generate_audiences' first.")
            )
            sys.exit(1)

        user_related_models = cmd.get_user_related_models()

        if not Audience.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    "No audiences found. Please run the 'generate_audiences' command first."
                )
            )
            return

        audience_names = [
            model._meta.verbose_name.title() for model in user_related_models
        ]
        audiences = Audience.objects.filter(name__in=audience_names)
        audiences_mapping = {aud.name: aud for aud in audiences}

        for model in user_related_models:
            audience_name = model._meta.verbose_name.title()
            if audience_name not in audiences_mapping:
                self.stdout.write(
                    self.style.WARNING(
                        f"Audience '{audience_name}' does not exist, skipping."
                    )
                )

        user_filter = Q()
        for model in user_related_models:
            user_filter |= Q(**{f"{model._meta.model_name}__isnull": False})

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

        if users_without_profiles:
            UserAnnouncementProfile.objects.bulk_create(
                [UserAnnouncementProfile(user=user) for user in users_without_profiles]
            )

        # Fetch or include newly created profiles
        user_profiles = list(
            UserAnnouncementProfile.objects.filter(user__in=related_users)
        )

        profiles_dict = {profile.user_id: profile for profile in user_profiles}

        existing_assignments = UserAudience.objects.filter(
            user_announce_profile__in=user_profiles
        ).values_list("user_announce_profile_id", "audience_id")

        # Create a set of existing profile-audience pairs to check for duplicates
        existing_assignments_set = set(existing_assignments)

        # Bulk assign audiences
        audience_assignments = []
        for model in user_related_models:
            related_user_ids = related_users.filter(
                **{f"{model._meta.model_name}__isnull": False}
            ).values_list("id", flat=True)

            for user_id in related_user_ids:
                if user_id in profiles_dict:
                    audience = audiences_mapping.get(model._meta.verbose_name.title())
                    if audience:
                        profile = profiles_dict[user_id]
                        # Check if the user-audience assignment already exists
                        if (profile.id, audience.id) not in existing_assignments_set:
                            audience_assignments.append(
                                UserAudience(
                                    user_announce_profile=profile, audience=audience
                                )
                            )

        # Perform bulk assignment of audiences
        if audience_assignments:
            UserAudience.objects.bulk_create(
                audience_assignments, ignore_conflicts=True
            )

        self.stdout.write(
            self.style.SUCCESS(
                "All users have been assigned to existing audiences successfully."
            )
        )
