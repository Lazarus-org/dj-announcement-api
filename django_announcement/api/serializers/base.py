from typing import Any, Dict

from rest_framework.serializers import ModelSerializer

from django_announcement.settings.conf import config
from django_announcement.utils.serialization import filter_non_empty_fields


class BaseFilteredSerializer(ModelSerializer):
    """Base serializer that filters out empty fields from the
    representation."""

    def to_representation(self, instance: Any) -> Dict[str, Any]:
        """Convert the instance to a representation format, filtering out empty
        fields if the setting is enabled.

        Args:
            instance (Any): A model instance being serialized.

        Returns:
            Dict[str, Any]: The filtered representation of the instance data.

        """
        data = super().to_representation(instance)

        # Apply filtering based on config setting
        if config.exclude_serializer_empty_fields:
            return filter_non_empty_fields(data)

        return data
