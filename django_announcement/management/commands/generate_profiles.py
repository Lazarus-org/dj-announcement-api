from typing import Dict, List

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, QuerySet

from django_announcement.management.commands.generate_audiences import Command as cmd
from django_announcement.models import Audience, UserAnnouncementProfile, UserAudience
from django_announcement.utils.user_model import UserModel


class Command(BaseCommand):
    """A Django management command to assign users to dynamically created
    audiences using the UserAnnouncementProfile model. It ensures that users
    are associated with audiences based on user-related models.

    Attributes:
    ----------
        PROCEED_CONFIRMATION: A set of valid user inputs for confirmation.

    """

    help = "Assign users to the dynamically created audiences using UserAnnouncementProfile model."

    PROCEED_CONFIRMATION = {"yes", "y"}

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

    @transaction.atomic
    def handle(self, *args: str, **kwargs: Dict[str, str]) -> None:
        """Execute the command to assign users to audiences. It checks if the
        audience generation command has been run and processes user assignments
        accordingly.

        Args:
        ----
            *args: Additional positional arguments.
            **kwargs: Keyword arguments, including 'skip-confirmation' to bypass user confirmation.

        """
        if (
            not kwargs.get("skip_confirmation")
            and not self._check_audience_generation()
        ):
            return

        try:
            user_related_models_dict = cmd.get_user_related_models()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error fetching user-related models: {e}")
            )
            return

        user_related_model_keys = list(user_related_models_dict.keys())
        user_related_model_values = list(user_related_models_dict.values())

        related_users = self._get_related_users(user_related_model_values)
        if not related_users:
            self.stdout.write(
                self.style.WARNING("No users found related to the provided models.")
            )
            return

        audiences_mapping = self._get_audiences_mapping(user_related_model_keys)
        if not audiences_mapping:
            self.stdout.write(
                self.style.WARNING(
                    "No valid audiences found, Please run 'generate_audiences' first. Exiting..."
                )
            )
            return

        self._create_user_profiles(related_users)

        audience_assignments = self._build_audience_assignments(
            user_related_model_keys,
            user_related_model_values,
            related_users,
            audiences_mapping,
        )
        self._bulk_assign_audiences(audience_assignments)

        self.stdout.write(
            self.style.SUCCESS(
                "All users have been assigned to existing audiences successfully."
            )
        )

    def _check_audience_generation(self) -> bool:
        """Check if the 'generate_audiences' command has been run.

        Returns:
        -------
            bool: True if the user has confirmed running 'generate_audiences', False otherwise.

        """
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

        if proceed not in self.PROCEED_CONFIRMATION:
            self.stdout.write(
                self.style.SUCCESS("Exiting... Please run 'generate_audiences' first.")
            )
            return False
        return True

    def _get_audiences_mapping(
        self, user_related_model_keys: List[str]
    ) -> Dict[str, Audience]:
        """Fetch and map existing audiences based on user-related models.

        Args:
        ----
            user_related_model_keys (List[str]): A list of keys for user-related models.

        Returns:
        -------
            Dict[str, Audience]: A mapping of audience names to Audience objects.

        """
        audience_names = [
            model._meta.verbose_name.title() for model in user_related_model_keys
        ]
        audiences = Audience.objects.filter(name__in=audience_names)
        audiences_mapping = {aud.name: aud for aud in audiences}

        missing_audiences = set(audience_names) - set(audiences_mapping.keys())
        if missing_audiences:
            self.stdout.write(
                self.style.WARNING(f"Missing audiences: {', '.join(missing_audiences)}")
            )

        return audiences_mapping

    def _get_related_users(self, user_related_model_values: List[str]) -> QuerySet:
        """Fetch related users based on user-related models.

        Args:
        ----
            user_related_model_values (List[str]): A list of values for user-related models.

        Returns:
        -------
            QuerySet: A QuerySet of related users.

        """
        user_filter = Q()
        for rel_name in user_related_model_values:
            user_filter |= Q(**{f"{rel_name}__isnull": False})

        return UserModel.objects.filter(user_filter).distinct()

    def _create_user_profiles(self, related_users: QuerySet) -> None:
        """Create user announcement profiles for users without profiles.

        Args:
        ----
            related_users QuerySet: A QuerySet of related users.

        """
        existing_profiles = UserAnnouncementProfile.objects.filter(
            user__in=related_users
        ).values_list("user_id", flat=True)
        users_without_profiles = related_users.exclude(id__in=existing_profiles)

        if users_without_profiles:
            UserAnnouncementProfile.objects.bulk_create(
                [UserAnnouncementProfile(user=user) for user in users_without_profiles],
                ignore_conflicts=True,
            )

    def _build_audience_assignments(
        self,
        user_related_model_keys: List[str],
        user_related_model_values: List[str],
        related_users: QuerySet,
        audiences_mapping: Dict[str, Audience],
    ) -> List[UserAudience]:
        """Build a list of audience assignments for users.

        Args:
        ----
            user_related_model_keys (List[str]): A list of keys for user-related models.
            user_related_model_values (List[str]): A list of values for user-related models.
            related_users (QuerySet): A QuerySet of related users.
            audiences_mapping (Dict[str, Audience]): A mapping of audience names to Audience objects.

        Returns:
        -------
            List[UserAudience]: A list of UserAudience assignments to be created.

        """
        user_profiles = UserAnnouncementProfile.objects.filter(user__in=related_users)
        profiles_dict = {profile.user_id: profile for profile in user_profiles}

        existing_assignments = UserAudience.objects.filter(
            user_announce_profile__in=user_profiles
        ).values_list("user_announce_profile_id", "audience_id")

        existing_assignments_set = set(existing_assignments)
        audience_assignments = []

        for model_key, rel_name in zip(
            user_related_model_keys, user_related_model_values
        ):
            related_user_ids = related_users.filter(
                **{f"{rel_name}__isnull": False}
            ).values_list("id", flat=True)

            for user_id in related_user_ids:
                if user_id in profiles_dict:
                    audience = audiences_mapping.get(
                        model_key._meta.verbose_name.title()
                    )
                    if (
                        audience
                        and (profiles_dict[user_id].id, audience.id)
                        not in existing_assignments_set
                    ):
                        audience_assignments.append(
                            UserAudience(
                                user_announce_profile=profiles_dict[user_id],
                                audience=audience,
                            )
                        )

        return audience_assignments

    def _bulk_assign_audiences(self, audience_assignments: List[UserAudience]) -> None:
        """Bulk assign audiences to users.

        Args:
        ----
            audience_assignments (List[UserAudience]): A list of UserAudience assignments to create.

        """
        if audience_assignments:
            UserAudience.objects.bulk_create(
                audience_assignments, ignore_conflicts=True
            )
