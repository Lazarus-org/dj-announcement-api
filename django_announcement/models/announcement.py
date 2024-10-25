from typing import List

from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Index,
    ManyToManyField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel
from django_announcement.repository.manager.announcement import (
    AnnouncementDataAccessLayer,
)
from django_announcement.settings.conf import config


class Announcement(TimeStampedModel):
    """A model to represent an announcement.

    This model contains the essential details for creating an announcement,
    including title, content, audience, and related metadata like publication dates.

    Attributes:
        title (CharField): The title of the announcement.
        content (TextField): The detailed content of the announcement.
        category (ForeignKey): A foreign key linking to the Category model for announcement classification.
        audience (CharField): The target audience for the announcement (e.g., Public, Internal, VIP).
        published_at (DateTimeField, optional): The date and time when the announcement is published.
        expires_at (DateTimeField, optional): The date and time when the announcement expires.
        attachment (FileField, optional): A file attachment for the announcement (e.g., flyer).

    Meta:
        db_table (str): The name of the database table.
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.
        indexes (List[Index]): Indexes for optimizing queries on title, category, and audience.

    Methods:
        __str__() -> str:
            Returns a string representation of the announcement including the title.

    """

    title = CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("The title of the announcement."),
        db_comment="The main title of the announcement.",
    )
    content = TextField(
        verbose_name=_("Content"),
        help_text=_("The content or description of the announcement."),
        db_comment="Detailed content or description of the announcement.",
    )
    category = ForeignKey(
        to="AnnouncementCategory",
        verbose_name=_("Category"),
        help_text=_("The category of the announcement."),
        db_comment="Foreign key linking to the Category model for announcement classification.",
        on_delete=CASCADE,
        related_name="announcements",
    )
    audience = ManyToManyField(
        to="Audience",
        through="AudienceAnnouncement",
        verbose_name=_("Audience"),
        help_text=_("The target audience for the announcement."),
        related_name="all_announcements",
    )
    published_at = DateTimeField(
        verbose_name=_("Published at"),
        help_text=_("The time when the announcement is published."),
        db_comment="Timestamp for when the announcement is published.",
        blank=True,
        null=True,
    )
    expires_at = DateTimeField(
        verbose_name=_("Expires at"),
        help_text=_("The time when the announcement expires."),
        db_comment="Timestamp for when the announcement expires.",
        blank=True,
        null=True,
    )
    attachment = FileField(
        verbose_name=_("Attachment"),
        help_text=_("An optional file attachment for the announcement (e.g., flyer)."),
        db_comment="Optional file attachment related to the announcement.",
        upload_to=config.attachment_upload_path,
        validators=config.attachment_validators or [],
        blank=True,
        null=True,
    )

    objects = AnnouncementDataAccessLayer()

    class Meta:
        db_table: str = "announcements"
        verbose_name: str = _("Announcement")
        verbose_name_plural: str = _("Announcements")
        indexes: List[Index] = [
            Index(fields=["title", "category"], name="announcement_idx"),
        ]

    def __str__(self) -> str:
        """Return a string representation of the announcement.

        Returns:
            str: A string representation of the announcement including the title.

        """
        return str(self.title)
