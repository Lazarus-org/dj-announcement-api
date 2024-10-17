from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoAnnouncementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_announcement"
    verbose_name = _("Django Announcement")
