from django.db.models import CASCADE, ForeignKey
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel


class UserAudience(TimeStampedModel):
    """Through model to link users and audiences for announcements."""

    user_announce_profile = ForeignKey(
        to="UserAnnouncementProfile",
        on_delete=CASCADE,
        related_name="user_audiences",
        verbose_name=_("User Profile"),
        help_text=_("The user profile associated with the audience."),
        db_comment="Foreign key to the UserAnnouncementProfile table.",
    )
    audience = ForeignKey(
        to="Audience",
        on_delete=CASCADE,
        related_name="audience_users",
        verbose_name=_("Audience"),
        help_text=_("The audience associated with the user profile."),
        db_comment="Foreign key to the Audience table.",
    )

    class Meta:
        db_table = "user_audience"
        verbose_name = _("User Audience")
        verbose_name_plural = _("User Audiences")
        unique_together = ("user_announce_profile", "audience")
