Roles
=====
This section outlines the various roles within ``django-announcement-api``, detailing their permissions, actions, and throttling limits for both API and admin interactions. By defining role-based access control, the system ensures secure and efficient management of announcements, while providing flexibility for different user levels. Whether for anonymous users with no access, authenticated users interacting via the API, or administrators managing the announcement system, these roles offer a structured way to control who can create, retrieve, update, or delete announcements. This role-based framework helps maintain security, optimize performance, and support scalable system management.

API Roles
---------

This section defines the user roles that interact with the `dj-announcement-api` and outlines their specific permissions, throttling limits, and actions available via the API. These roles allow for fine-grained control over who can retrieve, update, and delete announcements, and ensure that the system is scalable and secure for various levels of users.

1. Anonymous Users
~~~~~~~~~~~~~~~~~~
Anonymous users are those who are not authenticated within the Django application. By default, anonymous users do not have access to most of the features in the announcement API.

**Permissions**:
  - **List Announcements**: ❌ (Disabled)
  - **Retrieve Announcements**: ❌ (Disabled)

**Throttling**:
  - **Rate Limit**: N/A (No access)

**Use Case**:
  Anonymous users are generally restricted from interacting with the announcement system.

2. Authenticated Users
~~~~~~~~~~~~~~~~~~~~~~
Authenticated users are regular users who have logged in to the Django application. They have basic permissions to view announcements.

**Permissions**:
  - **List announcements**: ✅ (If ``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST`` is set to ``True``)
  - **Retrieve announcements**: ✅ (If ``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE`` is set to ``True``)

**Throttling**:
  - **Rate Limit**: ``30/minute`` (Configurable via ``DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE``)

**Use Case**:
  Authenticated users can view and retrieve their own announcements, but they cannot create or delete announcements.

3. Staff Users (Admin)
~~~~~~~~~~~~~~~~~~~~~~
Staff users (admin or elevated users) have more privileges in terms of managing announcements, depending on the configuration of the settings.

**Permissions**:
  - **List announcements**: ✅ (If allowed by ``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST``)
  - **Retrieve announcements**: ✅ (If allowed by ``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE``)

**Throttling**:
  - **Rate Limit**: ``100/minute`` (Configurable via ``DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE``)

**Use Case**:
  Staff users are responsible for maintaining the announcement system. They view all announcements in the system.


Customizing Roles with Extra Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The system also allows for more fine-grained control through the ``DJANGO_ANNOUNCEMENT_API_EXTRA_PERMISSION_CLASS`` setting. You can define additional custom permission classes that extend the base permissions, adding conditions for API access. This is useful when specific user groups or roles require specialized access to certain announcement features.

**Example**:
You can create a custom permission class to restrict access to only users with a particular role or attribute:

.. code-block:: python

    DJANGO_ANNOUNCEMENT_API_EXTRA_PERMISSION_CLASS = (
        "myapp.permissions.CustomPermissionClass"
    )

Role-Based Throttling
~~~~~~~~~~~~~~~~~~~~~
The package offers a **role-based throttling system**, allowing you to configure different API request rates for different user roles:

  - **Authenticated Users**: Throttled at a rate of ``30 requests/minute`` by default.
  - **Staff Users**: Throttled at a rate of ``100 requests/minute`` by default.
  - **Superusers**: No throttling applied.

This ensures that the API remains performant, and users with higher permissions are allowed to make more requests.

**Example Throttle Configuration**:

.. code-block:: python

    DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE = "30/minute"
    DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE = "100/minute"
    DJANGO_ANNOUNCEMENT_API_THROTTLE_CLASS = (
        "django_announcement.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"
    )

Summary of Role Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Role
     - List announcements
     - Retrieve announcements
     - Throttle Rate
   * - **Anonymous**
     - ❌
     - ❌
     - N/A
   * - **Authenticated**
     - ✅
     - ✅
     - 30/minute
   * - **Staff**
     - ✅
     - ✅
     - 100/minute

By configuring these roles, you ensure that each user type has access to the appropriate level of functionality within the announcement API, maintaining security and system stability.

----

Admin Role
----------

This section outlines the role of admins in interacting with the `dj-announcement-api` through the Django admin panel. Admin users have elevated privileges to manage announcements and their associated data.

1. Admin Users
~~~~~~~~~~~~~~
Admin users have comprehensive permissions to manage announcements, including creating, updating, deleting, and viewing both active and expired announcements.

**Permissions**:
  - **Create announcements**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION`` is set to ``True``)
  - **Modify announcements**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION`` is set to ``True``)
  - **Delete announcements**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION`` is set to ``True``)
  - **Module permission**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION`` is set to ``True``)


**Use Case**:
  Admin users are responsible for maintaining the announcement system, including managing audiences, categories, user announcement profiles and so on.


Inline Admin Interfaces
~~~~~~~~~~~~~~~~~~~~~~~
The admin panel includes two inline interfaces:
- **AudienceInline**: Manage audiences associated with announcements directly.
- **UserAudienceInline**: Manage audiences associated with user profiles directly.

**Permissions**:
  - **Create**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION`` is set to ``True``)
  - **Modify**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION`` is set to ``True``)
  - **Delete**: ✅ (If ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION`` is set to ``True``)


List Display
~~~~~~~~~~~~
The list view for announcements includes fields such as:
- ``ID``: Unique identifier for each announcement.
- ``Title``: Title of the announcement.
- ``Category``: The category of the announcement.
- ``Created at``: Creation time of the announcement.
- ``Expires at``: Expiration time of the announcement.

Filtering
~~~~~~~~~
Admins can filter announcements by:
- ``created_at``
- ``updated_at``
- ``category``

Search Functionality
~~~~~~~~~~~~~~~~~~~~
Search for announcements using:
- ``ID``
- ``Title``
- ``Content``
- ``audience name``

Pagination
~~~~~~~~~~
The admin list view displays **10 announcements per page** by default for better management of large lists.

Permissions Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~
Control admin permissions through settings:
- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION``: Controls "add" action.
- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION``: Controls "change" action.
- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION``: Controls "delete" action.
- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION``: Controls "module" permission.

Control inline admin permissions through settings:
- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION``: Controls "add" action.
- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION``: Controls "change" action.
- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION``: Controls "delete" action.


Most of the functionality within each admin interface adheres to these outlined guidelines, ensuring consistency and ease of management across all related models.