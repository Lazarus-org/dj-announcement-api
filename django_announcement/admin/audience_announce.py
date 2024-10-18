from django.contrib.admin import register

from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models.audience_announce import AudienceAnnouncement
from django_announcement.settings.conf import config


@register(AudienceAnnouncement, site=config.admin_site_class)
class AudienceAnnouncementAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + [
        "audience",
        "announcement",
        "created_at",
    ]
    list_display_links = ["audience"]
    search_fields = BaseModelAdmin.search_fields + [
        "announcement__title",
        "audience__name",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("audience", "announcement"),
            },
        ),
    ] + BaseModelAdmin.fieldsets
