from django_announcement.api.serializers.base import BaseFilteredSerializer
from django_announcement.models import AnnouncementCategory


class AnnouncementCategorySerializer(BaseFilteredSerializer):

    class Meta:
        model = AnnouncementCategory
        fields = [
            "id",
            "name",
            "description",
        ]
