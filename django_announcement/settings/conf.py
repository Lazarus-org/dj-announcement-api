from typing import Any, List

from django.conf import settings
from django.utils.module_loading import import_string

from django_announcement.constants.default_settings import (
    DefaultAdminSettings,
    DefaultAPISettings,
    DefaultAttachmentSettings,
    DefaultCommandSettings,
    DefaultPaginationAndFilteringSettings,
    DefaultSerializerSettings,
    DefaultThrottleSettings,
)
from django_announcement.constants.types import DefaultPath, OptionalPaths


# pylint: disable=too-many-instance-attributes
class AnnouncementConfig:
    """A configuration handler for the Django Announcement API, allowing
    settings to be dynamically loaded from Django settings with defaults
    provided through `DefaultSettings`.

    Attributes:
        include_serializer_full_details (bool): Whether full details are included in the serializer.
        exclude_serializer_empty_fields (bool): Whether empty fields should be excluded in the serializer.
        api_allow_list (bool): Whether the API allows listing announcements.
        api_allow_retrieve (bool): Whether the API allows retrieving single announcements.
        authenticated_user_throttle_rate (str): Throttle rate for authenticated users.
        staff_user_throttle_rate (str): Throttle rate for staff users.
        api_throttle_class (Optional[Type[Any]]): The class used for request throttling.
        api_pagination_class (Optional[Type[Any]]): The class used for pagination.
        api_extra_permission_class (Optional[Type[Any]]): An additional permission class for the API.
        api_parser_classes (Optional[List[Type[Any]]]): A list of parser classes used for the API.
        api_filterset_class (Optional[Type[Any]]): The class used for filtering announcements.
        api_ordering_fields (List[str]): Fields that can be used for ordering announcements in API queries.
        api_search_fields (List[str]): Fields that can be searched in API queries.
        admin_has_add_permission (bool): Whether the admin has permission to add announcements.
        admin_has_change_permission (bool): Whether the admin has permission to change announcements.
        admin_has_delete_permission (bool): Whether the admin has permission to delete announcements.
        admin_has_module_permission (bool): Whether the admin has module-level permissions.
        admin_inline_has_add_permission (bool): Whether the inline admin has permission to add announcements.
        admin_inline_has_change_permission (bool): Whether the inline admin has permission to change announcements.
        admin_inline_has_delete_permission (bool): Whether the inline admin has permission to delete announcements.
        admin_site_class (Optional[Type[Any]]): The class used for the admin site.
        generate_audiences_exclude_apps (List[str]): A list of apps excluded from audience generation.
        generate_audiences_exclude_models (List[str]): A list of models excluded from audience generation.

    """

    prefix = "DJANGO_ANNOUNCEMENT_"

    default_api_settings: DefaultAPISettings = DefaultAPISettings()
    default_serializer_settings: DefaultSerializerSettings = DefaultSerializerSettings()
    default_admin_settings: DefaultAdminSettings = DefaultAdminSettings()
    default_pagination_and_filter_settings: DefaultPaginationAndFilteringSettings = (
        DefaultPaginationAndFilteringSettings()
    )
    default_throttle_settings: DefaultThrottleSettings = DefaultThrottleSettings()
    default_command_settings: DefaultCommandSettings = DefaultCommandSettings()
    default_attachment_settings: DefaultAttachmentSettings = DefaultAttachmentSettings()

    def __init__(self) -> None:
        """Initialize the AnnouncementConfig, loading values from Django
        settings or falling back to the default settings."""

        self.admin_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_ADD_PERMISSION",
            self.default_admin_settings.admin_has_add_permission,
        )
        self.admin_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            self.default_admin_settings.admin_has_change_permission,
        )
        self.admin_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_DELETE_PERMISSION",
            self.default_admin_settings.admin_has_delete_permission,
        )
        self.admin_has_module_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_MODULE_PERMISSION",
            self.default_admin_settings.admin_has_module_permission,
        )
        self.admin_inline_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_ADD_PERMISSION",
            self.default_admin_settings.admin_inline_has_add_permission,
        )
        self.admin_inline_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_CHANGE_PERMISSION",
            self.default_admin_settings.admin_inline_has_change_permission,
        )
        self.admin_inline_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_DELETE_PERMISSION",
            self.default_admin_settings.admin_inline_has_delete_permission,
        )

        self.include_serializer_full_details: bool = self.get_setting(
            f"{self.prefix}SERIALIZER_INCLUDE_FULL_DETAILS",
            self.default_serializer_settings.include_serializer_full_details,
        )
        self.exclude_serializer_empty_fields: bool = self.get_setting(
            f"{self.prefix}SERIALIZER_EXCLUDE_EMPTY_FIELDS",
            self.default_serializer_settings.exclude_serializer_empty_fields,
        )

        self.api_allow_list: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_LIST", self.default_api_settings.allow_list
        )
        self.api_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_RETRIEVE",
            self.default_api_settings.allow_retrieve,
        )
        self.generate_audiences_exclude_apps: List[str] = self.get_setting(
            f"{self.prefix}GENERATE_AUDIENCES_EXCLUDE_APPS",
            self.default_command_settings.generate_audiences_exclude_apps,
        )
        self.generate_audiences_exclude_models: List[str] = self.get_setting(
            f"{self.prefix}GENERATE_AUDIENCES_EXCLUDE_MODELS",
            self.default_command_settings.generate_audiences_exclude_models,
        )
        self.attachment_upload_path: str = self.get_setting(
            f"{self.prefix}ATTACHMENT_UPLOAD_PATH",
            self.default_attachment_settings.upload_path,
        )
        self.attachment_validators: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ATTACHMENT_VALIDATORS",
            self.default_attachment_settings.validators,
        )
        self.authenticated_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}AUTHENTICATED_USER_THROTTLE_RATE",
            self.default_throttle_settings.authenticated_user_throttle_rate,
        )
        self.staff_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}STAFF_USER_THROTTLE_RATE",
            self.default_throttle_settings.staff_user_throttle_rate,
        )
        self.api_throttle_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_THROTTLE_CLASS",
            self.default_throttle_settings.throttle_class,
        )
        self.api_pagination_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGINATION_CLASS",
            self.default_pagination_and_filter_settings.pagination_class,
        )
        self.api_extra_permission_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_EXTRA_PERMISSION_CLASS",
            self.default_api_settings.extra_permission_class,
        )
        self.api_parser_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PARSER_CLASSES",
            self.default_api_settings.parser_classes,
        )
        self.api_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_FILTERSET_CLASS",
            self.default_pagination_and_filter_settings.filterset_class,
        )
        self.api_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_ORDERING_FIELDS",
            self.default_pagination_and_filter_settings.ordering_fields,
        )
        self.api_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_SEARCH_FIELDS",
            self.default_pagination_and_filter_settings.search_fields,
        )
        self.admin_site_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ADMIN_SITE_CLASS",
            self.default_admin_settings.admin_site_class,
        )

    def get_setting(self, setting_name: str, default_value: Any) -> Any:
        """Retrieve a setting from Django settings with a default fallback.

        Args:
            setting_name (str): The name of the setting to retrieve.
            default_value (Any): The default value to return if the setting is not found.

        Returns:
            Any: The value of the setting or the default value if not found.

        """
        return getattr(settings, setting_name, default_value)

    def get_optional_paths(
        self,
        setting_name: str,
        default_path: DefaultPath,
    ) -> OptionalPaths:
        """Dynamically load a method or class path on a setting, or return None
        if the setting is None or invalid.

        Args:
            setting_name (str): The name of the setting for the method or class path.
            default_path (Optional[Union[str, List[str]]): The default import path for the method or class.

        Returns:
            Optional[Union[Type[Any], List[Type[Any]]]]: The imported method or class or None
             if import fails or the path is invalid.

        """
        _path: DefaultPath = self.get_setting(setting_name, default_path)

        if _path and isinstance(_path, str):
            try:
                return import_string(_path)
            except ImportError:
                return None
        elif _path and isinstance(_path, list):
            try:
                return [import_string(path) for path in _path if isinstance(path, str)]
            except ImportError:
                return []

        return None


config: AnnouncementConfig = AnnouncementConfig()
