from django.db.models import Manager, QuerySet

from django_announcement.constants.types import Audiences, Categories
from django_announcement.repository.queryset.announcement import AnnouncementQuerySet


class AnnouncementDataAccessLayer(Manager):
    """Data Access Layer for the Announcement model.

    This class provides an interface for retrieving and manipulating
    Announcement objects by utilizing custom methods defined in the
    AnnouncementQuerySet.

    """

    def get_queryset(self) -> AnnouncementQuerySet:
        """Override the default get_queryset method to return an
        AnnouncementQuerySet instance.

        This ensures that any query made using this manager will utilize
        the custom methods and properties defined in the AnnouncementQuerySet.

        Returns:
            AnnouncementQuerySet: A queryset that allows chaining custom query methods.

        """
        return AnnouncementQuerySet(self.model, using=self._db)

    def all(self) -> QuerySet:
        """Retrieves all announcements.

        Returns:
            QuerySet: A queryset of all announcements.

        """
        return self.get_queryset()._join

    def active(self) -> QuerySet:
        """Retrieves active (published and not expired) announcements.

        Returns:
            QuerySet: A queryset of active announcements.

        """
        return self.get_queryset().active()

    def upcoming(self) -> QuerySet:
        """Retrieves announcements that are scheduled to be published in the
        future.

        Returns:
            QuerySet: A queryset of upcoming announcements.

        """
        return self.get_queryset().upcoming()

    def expired(self) -> QuerySet:
        """Retrieves announcements that have expired.

        Returns:
            QuerySet: A queryset of expired announcements.

        """
        return self.get_queryset().expired()

    def get_by_audience(self, audiences: Audiences) -> QuerySet:
        """Retrieves announcements targeted at specific audience(s).

        Args:
            audiences (Audiences): A single audience instance,
            audience ID, or an iterable of audience instances to filter announcements by.

        Returns:
            QuerySet: A queryset of announcements for the given audience(s).

        """
        return self.get_queryset().get_by_audience(audiences)

    def get_by_category(self, categories: Categories) -> QuerySet:
        """Retrieves announcements filtered by category(s).

        Args:
            categories (Categories): A single category instance,
            category ID, or an iterable of category instances to filter announcements by.

        Returns:
            QuerySet: A queryset of announcements for the given category(s).

        """
        return self.get_queryset().get_by_category(categories)
