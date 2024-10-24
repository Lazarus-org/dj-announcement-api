from django.db.models import CASCADE, ForeignKey
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel


class AudienceAnnouncement(TimeStampedModel):
    """Through model to manage the relationship between Announcements and
    Audiences."""

    announcement = ForeignKey(
        to="Announcement",
        on_delete=CASCADE,
        related_name="announcement_audiences",
        verbose_name=_("Announcement"),
        help_text=_("The announcement associated with the audience."),
        db_comment="Foreign key to the Announcement table, representing the announcement in this relationship.",
    )
    audience = ForeignKey(
        to="Audience",
        on_delete=CASCADE,
        related_name="audience_announcements",
        verbose_name=_("Audience"),
        help_text=_("The audience associated with the announcement."),
        db_comment="Foreign key to the Audience table, representing the audience in this relationship.",
    )

    class Meta:
        db_table = "audience_announcement"
        verbose_name = _("Audience Announcement")
        verbose_name_plural = _("Audience Announcements")
        unique_together = ("announcement", "audience")
