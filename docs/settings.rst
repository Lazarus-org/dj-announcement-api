Settings
=========

This section outlines the available settings for configuring the `dj-announcement-api` package. You can customize these settings in your Django project's `settings.py` file to tailor the behavior of the announcement system to your needs.

Example Settings
----------------

Below is an example configuration with default values:

.. code-block:: python

    DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION = False
    DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION = True
    DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS = None
    DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS = False
    DJANGO_ANNOUNCEMENT_SERIALIZER_EXCLUDE_EMPTY_FIELDS = False
    DJANGO_ANNOUNCEMENT_API_ALLOW_LIST = True
    DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE = True
    DJANGO_ANNOUNCEMENT_ATTACHMENT_VALIDATORS = []
    DJANGO_ANNOUNCEMENT_ATTACHMENT_UPLOAD_PATH = "announcement_attachments/"
    DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE = "30/minute"
    DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE = "100/minute"
    DJANGO_ANNOUNCEMENT_API_THROTTLE_CLASS = (
        "django_announcement.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"
    )
    DJANGO_ANNOUNCEMENT_API_PAGINATION_CLASS = "django_announcement.api.paginations.limit_offset_pagination.DefaultLimitOffSetPagination"
    DJANGO_ANNOUNCEMENT_API_EXTRA_PERMISSION_CLASS = None
    DJANGO_ANNOUNCEMENT_API_PARSER_CLASSES = [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ]
    DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS = None
    DJANGO_ANNOUNCEMENT_API_ORDERING_FIELDS = [
        "id",
        "published_at",
        "expires_at",
        "created_at",
        "updated_at",
    ]
    DJANGO_ANNOUNCEMENT_API_SEARCH_FIELDS = ["title", "content", "category__name"]
    DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS = []
    DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS = []

Settings Overview
-----------------

Below is a detailed description of each setting, so you can better understand and tweak them to fit your project's needs.


``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows adding new instances. Set this to ``False`` to disable Admin users to create new instances.


----

``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows modifying existing instances. Set this to ``False`` to disable Admin users to edit instances.

----

``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows deleting instances. Set this to ``False`` to disable Admin users to delete instances.

----

``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Determines whether a user has access to the admin management module, including all its features and functionality. Set this to ``False`` to hide the dj-announcement-api related admin.

----

``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin inline interface allows adding new instances. Set this to ``False`` to disable Admin users to create new inline instances.


----

``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``False``

**Description**: Controls whether the admin inline interface allows modifying existing instances. Set this to ``True`` to enable Admin users to edit inline instances.

----

``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin inline interface allows deleting instances. Set this to ``False`` to disable Admin users to delete inline instances.

----

``DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies A custom AdminSite class to apply on Admin interface. This allows for more customization on Admin interface, enabling you to apply your AdminSite class into `dj-announcement-api` Admin interface.

----

``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``False``

**Description**: When set to ``True``, API responses will include all announcement fields. By default, only essential fields are returned.

----

``DJANGO_ANNOUNCEMENT_SERIALIZER_EXCLUDE_EMPTY_FIELDS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``False``

**Description**: When set to ``True``, API responses will exclude any fields that does not have value.

----

``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Allows the listing of announcements via the API. Set to ``False`` to disable this feature.

----

``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``bool``

**Default**: ``True``

**Description**: Allows retrieving individual announcements via the API. Set to ``False`` to disable this feature.

----

``DJANGO_ANNOUNCEMENT_ATTACHMENT_VALIDATORS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Allows specifying a list of additional validators for attachment files in announcements. Each validator should be passed as a Python path string, which can be dynamically loaded and applied to the attachment. For example, to add custom file size or file type validation, include paths to custom validator functions or classes.

----

``DJANGO_ANNOUNCEMENT_ATTACHMENT_UPLOAD_PATH``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``str``

**Default**: ``"announcement_attachments/"``

**Description**: Specifies the upload path for attachment files in announcements.

----

``DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``str``

**Default**: ``"30/minute"``

**Description**: Sets the throttle rate (requests per minute, hour or day) for authenticated users in the API.

----

``DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: `str`

**Default**: `"100/minute"`

**Description**: Sets the throttle rate (requests per minute, hour or day) for staff (Admin) users in the API.

----

``DJANGO_ANNOUNCEMENT_API_THROTTLE_CLASS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``str``

**Default**: ``"django_announcement.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"``

**Description**:  Specifies the throttle class used to limit API requests. Customize this or set it to ``None`` if no throttling is needed or want to use ``rest_framework`` `DEFAULT_THROTTLE_CLASSES`.

----

``DJANGO_ANNOUNCEMENT_API_PAGINATION_CLASS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``str``

**Default**: ``"django_announcement.api.paginations.limit_offset_pagination.DefaultLimitOffSetPagination"``

**Description**: Defines the pagination class used in the API. Customize this if you prefer a different pagination style or set to ``None`` to disable pagination.

----

``DJANGO_ANNOUNCEMENT_API_EXTRA_PERMISSION_CLASS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies an additional permission class to extend the base permission (``IsAuthenticated``) for the API. This allows for more fine-grained access control, enabling you to restrict API access to users with a specific permission, in addition to requiring authentication.

----

``DJANGO_ANNOUNCEMENT_API_PARSER_CLASSES``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``List[str]``

**Default**:
  .. code-block:: python

    DJANGO_ANNOUNCEMENT_API_PARSER_CLASSES = [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ]

**Description**: Specifies the parsers used to handle API request data formats. You can modify this list to add your parsers or set ``None`` if no parser needed.

----

``DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Specifies the filter class for API queries. If you want to use this, you need to **install** and add ``django_filters`` to your `INSTALLED_APPS` and provide the path to the ``AnnouncementFilter`` class (``"django_ANNOUNCEMENT.api.filters.announcement_filter.AnnouncementFilter"``). Alternatively, you can use a custom filter class if needed.

in your settings.py:

.. code-block:: python

  INSTALLED_APPS = [
      # ...
      "django_filters",
      # ...
  ]

and then apply this setting:

.. code-block:: python

  # apply in settings.py

  DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS = (
      "django_announcement.api.filters.announcement_filter.AnnouncementFilter"
  )


``DJANGO_ANNOUNCEMENT_API_ORDERING_FIELDS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``List[str]``

**Default**: ``["id", "published_at", "expires_at", "created_at", "updated_at"]``

**Description**: Specifies the fields available for ordering in API queries, allowing the API responses to be sorted by these fields. you can see all available fields here

----

``DJANGO_ANNOUNCEMENT_API_SEARCH_FIELDS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``List[str]``

**Default**: ``["title", "content", "category__name"]``

**Description**: Specifies the fields that are searchable in the API, allowing users to filter results based on these fields.

----

``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Specifies a list of app labels that should be excluded when running the `generate_audiences` command. If certain apps should not be considered for audience generation, list them here. For example:

.. code-block:: python

   DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS = ["finance", "store"]

This setting prevents the `generate_audiences` command from scanning the specified apps when creating dynamic audiences.

----

``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Specifies a list of model names that should be excluded when running the generate_audiences command. If certain models should not be included in the audience generation process, define them here. For example:

.. code-block:: python

  DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS = ["CustomModel", "AnotherModel"]

This setting allows fine-tuned control over which models are excluded from audience creation, even if their app is not fully excluded.

----

All Available Fields
~~~~~~~~~~~~~~~~~~~~

These are all fields that are available for searching, ordering, and filtering in the announcements API with their recommended usage:

- ``id``: Unique identifier of the announcement (orderable, filterable).
- ``title``: The title or subject of the announcement (searchable).
- ``category``: The category of the announcement (filterable).
- ``content``: The body or description of the announcement (searchable).
- ``audience``: The audience receiving the announcement (filterable).
- ``created_at``: The time when the announcement was created (orderable, filterable).
- ``updated_at``: The time when the announcement was last updated (orderable, filterable).
- ``published_at``: The scheduled publication time of the announcement (filterable).
- ``expires_at``: The expiration time of the announcement (filterable).

.. note::
  Exercise caution when modifying search and ordering fields. **Avoid** using foreign key or joined fields (``audience``, ``category``) directly in **search fields**, as this may result in errors. if you want to use them, you should access their fields like: ``category__name``.
