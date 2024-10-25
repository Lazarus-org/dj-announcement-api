from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class DefaultAttachmentSettings:
    validators: Optional[List] = None
    upload_path: str = "announcement_attachments/"


@dataclass(frozen=True)
class DefaultCommandSettings:
    generate_audiences_exclude_apps: List[str] = field(default_factory=lambda: [])
    generate_audiences_exclude_models: List[str] = field(default_factory=lambda: [])


@dataclass(frozen=True)
class DefaultSerializerSettings:
    include_serializer_full_details: bool = False
    exclude_serializer_empty_fields: bool = False


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None
    admin_has_add_permission: bool = True
    admin_has_change_permission: bool = True
    admin_has_delete_permission: bool = True
    admin_has_module_permission: bool = True
    admin_inline_has_add_permission: bool = True
    admin_inline_has_change_permission: bool = False
    admin_inline_has_delete_permission: bool = True


@dataclass(frozen=True)
class DefaultThrottleSettings:
    authenticated_user_throttle_rate: str = "30/minute"
    staff_user_throttle_rate: str = "100/minute"
    throttle_class: str = (
        "django_announcement.api.throttlings.RoleBasedUserRateThrottle"
    )


@dataclass(frozen=True)
class DefaultPaginationAndFilteringSettings:
    pagination_class: str = (
        "django_announcement.api.paginations.DefaultLimitOffSetPagination"
    )
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(
        default_factory=lambda: [
            "id",
            "published_at",
            "expires_at",
            "created_at",
            "updated_at",
        ]
    )
    search_fields: List[str] = field(
        default_factory=lambda: ["title", "content", "category__name"]
    )


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class DefaultAPISettings:
    allow_list: bool = True
    allow_retrieve: bool = True
    extra_permission_class: Optional[str] = None
    parser_classes: List[str] = field(
        default_factory=lambda: [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.MultiPartParser",
            "rest_framework.parsers.FormParser",
        ]
    )
