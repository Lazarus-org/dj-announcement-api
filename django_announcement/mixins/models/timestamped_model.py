from django.db.models import DateTimeField, Model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(Model):
    """Abstract base model that includes created_at and updated_at fields.

    Any model that inherits from this class will automatically have the
    created_at and updated_at fields.

    """

    created_at = DateTimeField(
        verbose_name=_("Created at"),
        help_text=_("The time when the record was created."),
        db_comment="Timestamp for when the record was created.",
        default=timezone.now,
    )
    updated_at = DateTimeField(
        verbose_name=_("Updated at"),
        help_text=_("The time when the record was last updated."),
        db_comment="Timestamp for when the record was last updated.",
        auto_now=True,
    )

    class Meta:
        abstract = True
