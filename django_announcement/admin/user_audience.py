from django.contrib.admin import register

from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models.user_audience import UserAudience
from django_announcement.settings.conf import config
from django_announcement.utils.user_model import USERNAME_FIELD


@register(UserAudience, site=config.admin_site_class)
class UserAudienceAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + [
        "user_announce_profile",
        "audience",
        "created_at",
    ]
    list_display_links = ["user_announce_profile"]
    search_fields = BaseModelAdmin.search_fields + [
        f"user_announce_profile__user__{USERNAME_FIELD}",
        "user_announce_profile__user__id",
        "audience__name",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("user_announce_profile", "audience"),
            },
        ),
    ] + BaseModelAdmin.fieldsets
