from typing import Union, Iterable


from django_announcement.models.audience import Audience
from django_announcement.models.announcement_category import AnnouncementCategory

# Type Alias for Announcement QuerySet
Audiences = Union[Audience, int, Iterable[Audience]]
Categories = Union[AnnouncementCategory, int, Iterable[AnnouncementCategory]]
