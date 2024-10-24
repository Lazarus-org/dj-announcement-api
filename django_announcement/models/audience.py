from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from django_announcement.mixins.models.timestamped_model import TimeStampedModel


class Audience(TimeStampedModel):
    """A model to represent dynamic audience types.

    This model allows creating custom audience types dynamically
    for use in announcements.

    Attributes:
        name (CharField): The name of the audience type (e.g., Public, VIP).
        description (CharField, optional): A brief description of the audience.

    Meta:
        db_table (str): The name of the database table.
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.

    Methods:
        __str__() -> str:
            Returns a string representation of the audience type.

    """

    name = CharField(
        max_length=50,
        verbose_name=_("Audience Name"),
        help_text=_("The name of the audience type (e.g., Manager, Employee)."),
        db_comment="The name of the audience type.",
        unique=True,
    )
    description = CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("A brief description of the audience."),
        db_comment="Optional description of the audience type.",
        blank=True,
        null=True,
    )

    class Meta:
        db_table: str = "audiences"
        verbose_name: str = _("Audience")
        verbose_name_plural: str = _("Audiences")

    def __str__(self) -> str:
        return str(self.name)
