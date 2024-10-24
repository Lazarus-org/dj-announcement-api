from django_announcement.mixins.admin.inlines import BaseAudienceInline
from django_announcement.models.audience_announce import AudienceAnnouncement
from django_announcement.models.user_audience import UserAudience


class AudienceInline(BaseAudienceInline):
    """Inline admin interface for AudienceAnnouncement model.

    Attributes:
        model: The model associated with this inline.

    """

    model = AudienceAnnouncement


class UserAudienceInline(BaseAudienceInline):
    """Inline admin interface for UserAudience model.

    Attributes:
        model: The model associated with this inline.

    """

    model = UserAudience
