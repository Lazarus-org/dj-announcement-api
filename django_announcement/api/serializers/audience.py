from django_announcement.api.serializers.base import BaseFilteredSerializer
from django_announcement.models import Audience


class AudienceSerializer(BaseFilteredSerializer):

    class Meta:
        model = Audience
        fields = [
            "id",
            "name",
            "description",
        ]
