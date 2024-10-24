from django.db.models import CharField, TextField
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel


class AnnouncementCategory(TimeStampedModel):
    """A model to represent categories for announcements.

    This model is used to categorize announcements into different groups,
    such as Conferences, Meetings, or Webinars.

    Attributes:
        name (CharField): The name of the announcement category.
        description (TextField, optional): A brief description of the category.

    Meta:
        db_table (str): The name of the database table.
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.

    Methods:
        __str__() -> str:
            Returns a string representation of the announcement category.

    """

    name = CharField(
        max_length=100,
        verbose_name=_("Category Name"),
        help_text=_("The name of the announcement category."),
        db_comment="The name of the announcement category, such as Conference or Webinar.",
        unique=True,
    )
    description = TextField(
        verbose_name=_("Description"),
        help_text=_("A brief description of the announcement category."),
        db_comment="Optional description to provide more details about the category.",
        blank=True,
        null=True,
    )

    class Meta:
        db_table: str = "announcement_categories"
        verbose_name: str = _("Announcement Category")
        verbose_name_plural: str = _("Announcement Categories")

    def __str__(self) -> str:
        """Return a string representation of the announcement category.

        Returns:
            str: A string representation of the announcement category.

        """
        return str(self.name)
