from django.conf import settings
from django.db.models import CASCADE, ManyToManyField, OneToOneField
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel
from django_announcement.utils.user_model import get_username


class UserAnnouncementProfile(TimeStampedModel):
    """A model that links a user to multiple audiences for announcement
    targeting."""

    user = OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name=_("User"),
        help_text=_("The user associated with this profile."),
        db_comment="One-to-one relationship with the user.",
        related_name="announcement_profile",
        db_index=True,
    )
    audiences = ManyToManyField(
        to="Audience",
        through="UserAudience",
        related_name="users",
        verbose_name=_("Audiences"),
        help_text=_("Audiences to which this user belongs."),
    )

    class Meta:
        db_table: str = "user_announcement_profiles"
        verbose_name: str = _("User Announcement Profile")
        verbose_name_plural: str = _("User Announcement Profiles")

    def __str__(self) -> str:
        return get_username(self.user)
