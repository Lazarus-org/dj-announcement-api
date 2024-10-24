API Guide
=========

This section provides a detailed overview of the Django Announcement API, allowing users to manage announcements efficiently. The API exposes two main endpoints:


Announcements API
-----------------

The ``announcement/announcements/`` endpoint provides the following features:

- **List active announcements**:

  Fetches all active announcements for the authenticated user (all announcements for admin users). Controlled by the ``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST`` setting.

- **Retrieve an announcement**:

  Retrieves a specific active announcement by its ID. Controlled by the ``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE`` setting.


Example Responses
-----------------

Here are some examples of responses for each action:


**List announcements with full details**:

.. code-block:: text

   GET /announcement/announcements/

   Response:
   HTTP/1.1 200 OK
   Content-Type: application/json

   "results": [
        {
            "id": 1,
            "title": "test announcement",
            "content": "some content",
            "category": {
                "id": 1,
                "name": "test category",
                "description": "something!"
            },
            "audience": [
                {
                    "id": 1,
                    "name": "new audience",
                    "description": null
                },
                {
                    "id": 2,
                    "name": "another audience",
                    "description": null
                },
            ],
            "published_at": "2024-10-18T08:49:52Z",
            "expires_at": null,
            "attachment": null,
            "created_at": "2024-10-18T08:49:09Z",
            "updated_at": "2024-10-18T09:10:41.743564Z"
        }
   ]

If the ``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS`` setting is ``True``, this detailed response will be returned for all users.

**List announcements with simplified data**:

.. code-block:: text

   GET /announcement/announcements/

   Response:
   HTTP/1.1 200 OK
   Content-Type: application/json

   "results": [
        {
            "id": 1,
            "title": "first announcement",
            "content": "some content",
            "category": {
                "id": 1,
                "name": "test category",
                "description": "something!"
            },
            "published_at": "2024-10-18T08:49:52Z",
            "expires_at": null,
            "attachment": null,
            "created_at": "2024-10-18T08:49:09Z",
            "updated_at": "2024-10-18T09:10:41.743564Z"
        },

      ...
   ]

This response is returned when ``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS`` is set to ``False``. Admins always see full details.


.. note::

 you can exclude Any fields with a ``null`` value in the response output by adding this config in your ``settings.py``:
.. code-block:: python

   DJANGO_ANNOUNCEMENT_SERIALIZER_EXCLUDE_NULL_FIELDS = True

Throttling
----------

The API includes a built-in throttling mechanism that limits the number of requests a user can make based on their role. You can customize these throttle limits in the settings file.

To specify the throttle rates for authenticated users and staff members, add the following in your settings:

.. code-block:: ini

   DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE = "100/day"
   DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE = "60/minute"

These settings limit the number of requests users can make within a given timeframe.

**Note:** You can define custom throttle classes and reference them in your settings.


Filtering, Ordering, and Search
-------------------------------

The API supports filtering, ordering, and searching of announcements. Filter Class can be applied optionally, allowing users to narrow down results.

Options include:

- **Filtering**: By default filtering feature is not included, If you want to use this, you need to add ``django_filters`` to your `INSTALLED_APPS` and provide the path to the ``AnnouncementFilter`` class (``"django_announcement.api.filters.announcement_filter.AnnouncementFilter"``). Alternatively, you can use a custom filter class if needed.

  - **Note**: for more clarification, refer to the `DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS` in :doc:`Settings <settings>` section.

- **Ordering**: Results can be ordered by fields such as ``id``, ``timestamp``, or ``public``.

- **Search**: You can search fields like ``verb`` and ``description``.

These fields can be customized by adjusting the related configurations in your Django settings.


Pagination
----------

The API supports limit-offset pagination, with configurable minimum, maximum, and default page size limits. This controls the number of results returned per page.

Permissions
-----------

The base permission for all endpoints is ``IsAuthenticated``, meaning users must be logged in to access the API. You can extend this by creating custom permission classes to implement more specific access control.

For instance, you can allow only specific user roles to perform certain actions.

Parser Classes
--------------

The API supports multiple parser classes that control how data is processed. The default parsers include:

- ``JSONParser``
- ``MultiPartParser``
- ``FormParser``

You can modify parser classes by updating the API settings to include additional parsers or customize the existing ones to suit your project.

----

Each feature can be configured through the Django settings file. For further details, refer to the :doc:`Settings <settings>` section.
