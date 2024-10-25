Quick Start
===========

This section provides a fast and easy guide to getting the `dj-announcement-api` package up and running in your Django project. Follow the steps below to quickly set up the package and start using it.

1. Install the Package
----------------------

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

.. code-block:: bash

   $ pip install dj-announcement-api

**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

.. code-block:: bash

   $ poetry add dj-announcement-api

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

.. code-block:: bash

   $ pipenv install dj-announcement-api


The package requires ``djangorestframework`` for API support. If it's not already installed in your project, you can install it using one of the above methods:

**Using pip:**

.. code-block:: bash

  $ pip install djangorestframework

2. Add to Installed Apps
------------------------

After installing the necessary packages, ensure that both ``rest_framework`` and ``django_announcement`` are added to the ``INSTALLED_APPS`` in your Django ``settings.py`` file:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "rest_framework",  # Required for API support
       "django_announcement",
       # ...
   ]

3. (Optional) Configure API Filters
-----------------------------------

To enable filtering of announcements through the API, install ``django-filter``, include ``django_filters`` in your ``INSTALLED_APPS`` and configure the filter settings.

Install ``django-filter`` using one of the above methods:

**Using pip:**

.. code-block:: bash

   $ pip install django-filter


Add `django_filters` to your `INSTALLED_APPS`:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "django_filters",
       # ...
   ]

Then, set the filter class configuration in your ``settings.py``:

.. code-block:: python

   DJANGO_announcement_API_FILTERSET_CLASS = (
       "django_announcement.api.filters.announcement_filter.AnnouncementFilter"
   )

You can also define your custom `FilterClass` and reference it in here if needed. This allows you to customize the filtering behavior according to your requirements.


4. Apply Migrations
-------------------

Run the following command to apply the necessary migrations:

.. code-block:: bash

   python manage.py migrate


5. Add Announcement API URLs
----------------------------

Include the announcement API routes in your project’s `urls.py` file:

.. code-block:: python

   from django.urls import path, include

   urlpatterns = [
       # ...
       path("announcement/", include("django_announcement.api.routers")),
       # ...
   ]

6. Generate Audiences and Profiles
----------------------------------

After setting up the package and applying the migrations, run the management commands to generate the necessary audiences based on user related models and generate announcement profiles for users to assign audience to them.

First, generate the audiences using the ``generate_audiences`` command:

.. code-block:: shell

   $ python manage.py generate_audiences

Then, assign users to these audiences by running the ``generate_profiles`` command:

.. code-block:: shell

   $ python manage.py generate_profiles


7. Create Announcements via Django Admin
----------------------------------------

Now, you can create announcements using the Django admin interface.

- Log in to the Django admin site.
- Navigate to the **Announcements** section.
- Click **Add Announcement** to create a new announcement, filling out the required fields such as title, content and category.
- Optionally, select the target audiences and attach files if needed.

Once saved, your announcements will be available to the users assigned to the relevant audiences.


8. Verify Announcements
-----------------------

Once announcements are created, they can be viewed through the API endpoints. To test and verify the creation, make a request to the relevant endpoint, for example:

.. code-block:: bash

   curl -X GET http://localhost:8000/announcement/annoucements/

This will return a list of announcements created in the admin.

----

With the setup complete, the ``dj-announcement-api`` is ready for use in your project. For further customizations and settings, refer to the :doc:`API Guide <api_guide>` and :doc:`Settings <settings>` sections.

