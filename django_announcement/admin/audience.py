from django.contrib.admin import register

from django_announcement.mixins.admin.base import BaseModelAdmin
from django_announcement.models.audience import Audience
from django_announcement.settings.conf import config


@register(Audience, site=config.admin_site_class)
class AudienceAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ["name", "created_at", "updated_at"]
    list_display_links = ["name"]
    search_fields = BaseModelAdmin.search_fields + ["name", "description"]
    fieldsets = [
        (
            None,
            {
                "fields": ("name", "description"),
            },
        ),
    ] + BaseModelAdmin.fieldsets
