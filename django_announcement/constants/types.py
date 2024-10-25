from typing import Any, Iterable, List, Optional, Type, Union

from django_announcement.models.announcement_category import AnnouncementCategory
from django_announcement.models.audience import Audience

# Type Alias for Announcement QuerySet
Audiences = Union[Audience, int, Iterable[Audience]]
Categories = Union[AnnouncementCategory, int, Iterable[AnnouncementCategory]]

# Type Alias for config class
DefaultPath = Optional[Union[str, List[str]]]
OptionalPaths = Optional[Union[Type[Any], List[Type[Any]]]]
