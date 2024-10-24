from django.db.models import Q, QuerySet
from django.utils.timezone import now

from django_announcement.constants.types import Audiences, Categories
from django_announcement.models.announcement_category import AnnouncementCategory
from django_announcement.models.audience import Audience


class AnnouncementQuerySet(QuerySet):
    """Custom queryset for the Announcement model.

    This class provides custom query methods to filter announcements based on
    different criteria, such as their publication status, audience, category,
    and scheduling. It optimizes query performance by selecting and prefetching
    related fields in a centralized manner.

    Methods:
        active(): Filters announcements that are currently published and not expired.
        upcoming(): Filters announcements scheduled for future publication.
        expired(): Filters announcements that have already expired.
        by_audience(audience_id: int): Filters announcements by target audience ID.
        by_category(category_id: int): Filters announcements by category ID.

    """

    @property
    def _join(self) -> QuerySet:
        """Apply select_related and prefetch_related to optimize queries.

        Returns:
            QuerySet: The queryset with related fields selected and prefetched.

        """
        return self.select_related(
            "category",
        ).prefetch_related("audience")

    def active(self) -> QuerySet:
        """Filter announcements that are currently active (published and not
        expired).

        Returns:
            QuerySet: A queryset containing active announcements.

        """
        _now = now()
        return self._join.filter(
            Q(published_at__lte=_now) | Q(published_at__isnull=True),
            Q(expires_at__gte=_now) | Q(expires_at__isnull=True),
        )

    def upcoming(self) -> QuerySet:
        """Filter announcements that are scheduled to be published in the
        future.

        Returns:
            QuerySet: A queryset containing announcements with a future publication date.

        """
        return self._join.filter(published_at__gt=now())

    def expired(self) -> QuerySet:
        """Filter announcements that have expired.

        Returns:
            QuerySet: A queryset containing expired announcements.

        """
        return self._join.filter(expires_at__lt=now())

    def get_by_audience(self, audiences: Audiences) -> QuerySet:
        """Filter announcements by the target audience(s).

        Args:
            audiences (Audiences): A single audience instance,
            audience ID, or an iterable of audience instances.

        Returns:
            QuerySet: A queryset containing announcements for the specified audience(s).

        """
        if isinstance(audiences, (int, Audience)):
            audiences = [audiences]

        return self._join.filter(audience__in=audiences).distinct()

    def get_by_category(self, categories: Categories) -> QuerySet:
        """Filter announcements by target category(s).

        Args:
            categories (Categories): A single category instance,
            category ID, or an iterable of category instances.

        Returns:
            QuerySet: A queryset containing announcements in the specified category(s).

        """
        if isinstance(categories, (int, AnnouncementCategory)):
            categories = [categories]

        return self._join.filter(category__in=categories).distinct()
