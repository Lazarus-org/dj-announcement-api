from typing import Optional

from django.contrib.admin import ModelAdmin
from django.http import HttpRequest

from django_announcement.settings.conf import config


class BasePermissionControlMixin:
    """A base mixin to control the add, change, delete permissions in the
    Django admin."""

    permission_prefix = ""

    def has_add_permission(
        self, request: HttpRequest, obj: Optional[ModelAdmin] = None
    ) -> bool:
        """Determines if the user has permission to add a new instance of the
        model."""
        return getattr(config, f"{self.permission_prefix}has_add_permission")

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[ModelAdmin] = None
    ) -> bool:
        """Determines if the user has permission to change an existing instance
        of the model."""
        return getattr(config, f"{self.permission_prefix}has_change_permission")

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[ModelAdmin] = None
    ) -> bool:
        """Determines if the user has permission to delete an existing instance
        of the model."""
        return getattr(config, f"{self.permission_prefix}has_delete_permission")


class AdminPermissionControlMixin(BasePermissionControlMixin):
    """A mixin that controls the ability to add, change, or delete objects and
    module permission in the Django admin."""

    permission_prefix = "admin_"

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Determines if the user has any permission in the given app label."""
        return getattr(config, f"{self.permission_prefix}has_module_permission")


class InlinePermissionControlMixin(BasePermissionControlMixin):
    """A mixin that controls the ability to add, change, or delete inline
    objects in the Django admin."""

    permission_prefix = "admin_inline_"
