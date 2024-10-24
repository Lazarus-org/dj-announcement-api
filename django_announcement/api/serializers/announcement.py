from django_announcement.api.serializers.audience import AudienceSerializer
from django_announcement.api.serializers.base import BaseFilteredSerializer
from django_announcement.api.serializers.category import AnnouncementCategorySerializer
from django_announcement.models.announcement import Announcement


class AnnouncementSerializer(BaseFilteredSerializer):
    """Serializer for detailed event data, used for staff users or detailed
    responses."""

    category = AnnouncementCategorySerializer(read_only=True)
    audience = AudienceSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "content",
            "category",
            "audience",
            "published_at",
            "expires_at",
            "attachment",
            "created_at",
            "updated_at",
        ]


class SimpleAnnouncementSerializer(BaseFilteredSerializer):
    category = AnnouncementCategorySerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "content",
            "category",
            "attachment",
            "created_at",
            "published_at",
            "expires_at",
        ]
