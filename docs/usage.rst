Usage
=====

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of the Django admin panels for managing announcements, announcement categories, audiences, user announcement profile and Manager methods for handling announcements.

Admin Site
----------

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your Django settings. Otherwise, Django may raise the following error during checks:

.. code-block:: shell

  ERRORS:
  <class 'django_announcement.admin.announcement_profile.UserAnnouncementProfileAdmin'>:
  (admin.E039) An admin for model "User" has to be registered to be referenced by UserAnnouncementProfileAdmin.autocomplete_fields.


To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class instance

.. code-block:: python

  DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS = "path.to.your.custom.site"

example of a custom Admin Site:

.. code-block:: python

  from django.contrib.admin import AdminSite


  class CustomAdminSite(AdminSite):
      site_header = "Custom Admin"
      site_title = "Custom Admin Portal"
      index_title = "Welcome to the Custom Admin Portal"


  # Instantiate the custom admin site as example
  example_admin_site = CustomAdminSite(name="custom_admin")

and then reference the instance like this:

.. code-block:: python

  DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS = "path.to.example_admin_site"

This setup allows `dj-announcement-api` to use your custom admin site for it's Admin interface, preventing any errors and ensuring a smooth integration with the custom admin interface.


Announcements Admin Panel
-------------------------

The ``AnnouncementAdmin`` class provides a comprehensive admin interface for managing announcements in the Django admin panel. The features and functionality are described below:


Inline Admin Interfaces
~~~~~~~~~~~~~~~~~~~~~~~

The ``AnnouncementAdmin`` panel includes two inline admin interfaces that allow admins to view and manage related models directly from the announcement page:

- ``AudienceInline``:

  Displays and manages the audiences associated with each announcement. Admins can view or add audience directly within the announcement details page.


List Display
~~~~~~~~~~~~

The list view for announcements includes the following fields:

- ``ID``: The unique identifier for each announcement.
- ``Title``: The announcement title or a summary.
- ``Category``: The category of the announcement.
- ``Created at``: Creation time of the announcement.
- ``Expires at``: Expiration time of the announcement.

This view helps admins get a quick overview of the announcements and their current status.

Filtering
~~~~~~~~~

Admins can filter the list of announcements based on the following fields:

- ``created_at``: Filter by the creation time of the announcement.
- ``updated_at``: Filter by the time that the announcement last updated.
- ``category``: Filter by announcement category.

These filters make it easier to find specific announcements or groups of announcements based on category or time.

Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for announcements using the following fields:

- ``ID``: The unique identifier of the announcement.
- ``Title``: The Title of the announcement.
- ``Content``: The content of the announcement.
- ``Audience Name``: The name of the audience associated with the announcement.

This search functionality enables quick access to specific announcements by key identifiers.

Pagination
~~~~~~~~~~

The admin list view displays **10 announcements per page** by default. This can help improve load times and make it easier for admins to manage large lists of announcements.

Permissions Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

The admin permissions for ``add``, ``change``, and ``delete`` actions and also ``module`` permission can be controlled through the following Django settings:

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION``: Controls whether the "add" action is available in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION``: Controls whether the "change" action is allowed in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION``: Controls whether the "delete" action is available in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION``: Determines whether a user has access to the admin management module, including all its features and functionality. Defaults to ``True``.


The admin permissions for ``add``, ``change``, and ``delete`` actions can be controlled through the following Django settings:

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION``: Controls whether the "add" action is available in the AudienceInline and UserAudienceInline Admin. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION``: Controls whether the "change" action is allowed in the AudienceInline and UserAudienceInline Admin. Defaults to ``False``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION``: Controls whether the "delete" action is available in the AudienceInline and UserAudienceInline Admin. Defaults to ``True``.

----

Announcement Categories Admin Panel
------------------------------------

The ``AnnouncementCategoryAdmin`` class provides an admin interface for managing announcement categories. Key features include:

List Display
~~~~~~~~~~~~

The list view for categories includes the following fields:

- ``ID``: The unique identifier of the category.
- ``Name``: The name of the category.
- ``Created at``: The time the category was created.
- ``Updated at``: The time the category was last updated.

This allows for a quick overview of available announcement categories.

Filtering
~~~~~~~~~

Admins can filter categories by:

- ``Created at``: Filter by the creation time of the category.
- ``Updated at``: Filter by the time the category was last updated.

Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for categories using:

- ``Name``: The name of the category.
- ``Description``: The description of the category.

Fieldsets
~~~~~~~~~

The admin panel displays the following fields when editing a category:

- ``ID``: The unique identifier of the category.
- ``Name``: The name of the category.
- ``Description``: A description of the category.

----

Audiences Admin Panel
---------------------

The ``AudienceAdmin`` class provides a user-friendly admin interface for managing audiences in the Django admin panel. Key features are described below:

Inline Admin Interfaces
~~~~~~~~~~~~~~~~~~~~~~~

The ``AudienceAdmin`` panel includes inline admin interfaces for managing related models:

- ``UserAudienceInline``:

  Allows admins to view and manage users associated with a specific audience directly within the audience details page.

List Display
~~~~~~~~~~~~

The list view for audiences includes the following fields:

- ``ID``: The unique identifier for each audience.
- ``Name``: The name of the audience.
- ``Created at``: The creation time of the audience.
- ``Updated at``: A time that the audience was last updated.

This display helps admins quickly view and manage different audience groups.

Filtering
~~~~~~~~~

Admins can filter the list of audiences based on the following fields:

- ``created_at``: Filter by the creation date of the audience.
- ``created_at``: Filter by the last updated date of the audience.

Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for audiences using the following fields:

- ``ID``: The unique identifier of the audience.
- ``Name``: The name of the audience.
- ``Description``: The description of the audience.

Pagination
~~~~~~~~~~

The admin list view shows **10 audiences per page** by default to improve load times and manageability.

----

User Announcement Profiles Admin Panel
--------------------------------------

The ``UserAnnouncementProfileAdmin`` class allows admins to manage the relationship between users and their assigned audiences.

Inline Admin Interfaces
~~~~~~~~~~~~~~~~~~~~~~~

The admin interface includes the following inline:

- ``UserAudienceInline``:

  Allows admins to view or manage the audiences assigned to a specific user from the user announcement profile page.

List Display
~~~~~~~~~~~~

The list view for user profiles includes the following fields:

- ``ID``: The unique identifier for each profile.
- ``User``: The associated user for the profile.
- ``Created at``: The creation time of the profile.
- ``Updated at``: The last updated time of the profile.

This helps admins manage user profiles and their audience relationships efficiently.

Filtering
~~~~~~~~~

Admins can filter user profiles by the following fields:

- ``created_at``: Filter by the creation date of the profile.
- ``created_at``: Filter by the last updated date of the audience.

Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for user profiles using the following fields:

- ``ID``: The unique identifier for each profile.
- ``User ID``: The Unique identifier of the associated user.
- ``User name``: The username of the associated user.
- ``Audience name``: The name of the assigned audience.

Pagination
~~~~~~~~~~

The admin list view shows **10 user profiles per page** by default to optimize load times.

----

Audience Announcements Admin Panel
----------------------------------

The ``AudienceAnnouncementAdmin`` class provides an interface to manage the relationship between audiences and announcements.

List Display
~~~~~~~~~~~~

The list view includes the following fields:

- ``ID``: The unique identifier of the AudienceAnnouncement.
- ``Audience``: The name of the audience.
- ``Announcement``: The associated announcement title.
- ``Created at``: The time the association was created.

Filtering and search options help manage and explore audience-announcement pairs.

Filtering
~~~~~~~~~

Admins can filter categories by:

- ``Created at``: Filter by the creation time of the AudienceAnnouncement.
- ``Updated at``: Filter by the time the category was last updated.


Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for audience-announcement relations by:

- ``ID``: The unique identifier of the audience-announcement.
- ``Announcement Title``: The title of the announcement.
- ``Audience Name``: The name of the audience.


User Audience Admin Panel
-------------------------

The ``UserAudienceAdmin`` class provides an admin interface for managing user-audience relationships.

List Display
~~~~~~~~~~~~

The list view includes the following fields:

- ``ID``: The unique identifier for each user-audience.
- ``User Announcement Profile``: The user profile linked to the audience.
- ``Audience``: The audience assigned to the user.
- ``Created at``: The time the user was assigned to the audience.

This makes managing user-audience relations straightforward.

Search Functionality
~~~~~~~~~~~~~~~~~~~~

Admins can search for user-audience relations by:

- ``ID``: The unique identifier for each user-audience.
- ``User Name``: The username of the associated user.
- ``User ID``: The ID of the user.
- ``Audience Name``: The name of the audience.


----

AnnouncementDataAccessLayer (Manager)
-------------------------------------

The ``django_announcement`` app provides a Manager Class ``AnnouncementDataAccessLayer`` with various methods to interact with announcements in different contexts. Users typically use `Announcement.objects.all()` to retrieve announcements, but other methods are available for querying specific subsets of announcements. Below is an overview of the available methods:


Return All Announcements
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``all`` method retrieves all announcements from the database.

**Method Signature**

.. code-block:: python

    from django_announcement.models.announcement import Announcement

    Announcement.objects.all()

**Returns:**

- A ``QuerySet`` of all announcements in the system.

**Example Usage:**

To retrieve all announcements:

.. code-block:: python

    from django_announcement.models.announcement import Announcement

    all_announcements = Announcement.objects.all()


Return Active Announcements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``active`` method retrieves only the announcements that are currently active (published and not expired).

**Method Signature**

.. code-block:: python

    from django_announcement.models.announcement import Announcement

    Announcement.objects.active()

**Returns:**

- A ``QuerySet`` of active announcements.

**Example Usage:**

To retrieve all active announcements:

.. code-block:: python

    active_announcements = Announcement.objects.active()


Return Upcoming Announcements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``upcoming`` method retrieves announcements that are scheduled to be published in the future.

**Method Signature**

.. code-block:: python

    from django_announcement.models.announcement import Announcement

    Announcement.objects.upcoming()

**Returns:**

- A ``QuerySet`` of announcements scheduled for future publication.

**Example Usage:**

To retrieve all upcoming announcements:

.. code-block:: python

    upcoming_announcements = Announcement.objects.upcoming()


Return Expired Announcements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``expired`` method retrieves announcements that have already expired.

**Method Signature**

.. code-block:: python

    from django_announcement.models.announcement import Announcement

    Announcement.objects.expired()

**Returns:**

- A ``QuerySet`` of expired announcements.

**Example Usage:**

To retrieve all expired announcements:

.. code-block:: python

    expired_announcements = Announcement.objects.expired()


Retrieve Announcements by Audience
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``get_by_audience`` method retrieves announcements targeted at specific audience(s).

**Method Signature**

.. code-block:: python

    from django_announcement.models.announcement import Announcement


    Announcement.objects.get_by_audience(audiences)

**Arguments:**

- **audiences** (``Audiences``):
  An audience instance, audience ID, or an iterable of audience instances to filter announcements by.

**Returns:**

- A ``QuerySet`` of announcements for the given audience(s).

**Example Usage:**

To retrieve announcements for a specific audience:

.. code-block:: python

    specific_audience = Audience.objects.get(id=1)
    audience_announcements = Announcement.objects.get_by_audience(specific_audience)


Retrieve Announcements by Category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``get_by_category`` method retrieves announcements filtered by specific category(s).

**Method Signature**

.. code-block:: python

    from django_announcement.models import Announcement


    Announcement.objects.get_by_category(categories)

**Arguments:**

- **categories** (``Categories``):
  A category instance, category ID, or an iterable of category instances to filter announcements by.

**Returns:**

- A ``QuerySet`` of announcements for the given category(s).

**Example Usage:**

To retrieve announcements for a specific category:

.. code-block:: python

    specific_category = Category.objects.get(id=2)
    category_announcements = Announcement.objects.get_by_category(specific_category)


generate_audiences Command
--------------------------

The ``generate_audiences`` command dynamically creates audiences based on models related to the ``User``. It allows filtering out specific apps and models through configuration settings, and includes an optional user confirmation step before proceeding.

Command Overview
~~~~~~~~~~~~~~~~

This command scans for related models in the ``User`` (excluding those defined in the settings), confirms the list of models with the user, and creates audiences if they don't already exist. It is useful for dynamically creating target audiences for announcements based on your application's data models.

Settings
~~~~~~~~

This command is influenced by two key settings:

- ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS``:
  A list of app labels to exclude from the audience generation process.

- ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS``:
  A list of model names to exclude from the audience generation process.

These settings allow for fine-grained control over which models are considered for audience creation.

Usage
~~~~~

The command can be run using Django's ``manage.py`` utility:

.. code-block:: bash

   $ python manage.py generate_audiences

Optional Arguments
~~~~~~~~~~~~~~~~~~

- ``--skip-confirmation``:
  Skips the user confirmation prompt and proceeds directly to creating audiences.

Example usage:

.. code-block:: bash

   $ python manage.py generate_audiences --skip-confirmation

Command Flow
~~~~~~~~~~~~

1. **Retrieve Related Models**:
   The command first retrieves all models related to the ``User`` by checking the relationships. It filters out any models and apps specified in the ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS`` and ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS`` settings.

2. **Prompt for Confirmation**:
   The command lists the related models found and asks for confirmation from the user to proceed. If the ``--skip-confirmation`` flag is provided, this step is bypassed.

3. **Create Audiences**:
   For each related model that doesn't already have a corresponding audience, the command creates a new audience and saves it in the database. It checks the existing audiences by their name to avoid duplications.

Example Output
~~~~~~~~~~~~~~

When running the command, the following example output might be displayed:

.. code-block:: text

   The following related models were found:
   1. User Profile
   2. Organization

   Are these the correct target models? Type 'y' to proceed or 'n' to modify settings: y
   Created audience: User Profile
   Created audience: Organization
   Finished creating audiences!

If no new audiences are needed, you would see:

.. code-block:: text

   No new audiences needed to be created.


generate_profiles Command
-------------------------

The ``generate_profiles`` command assigns users to dynamically created audiences using the ``UserAnnouncementProfile`` model. It ensures that users are correctly associated with audiences based on user-related models in the database. This command should be run after the ``generate_audiences`` command to link users to the relevant audiences.

Command Overview
~~~~~~~~~~~~~~~~

This command checks if the audience generation has been completed, then proceeds to create user profiles if they do not already exist. It builds and assigns audience-user relationships dynamically, based on the user-related models detected in the system.

Usage
~~~~~

The command can be run using Django's ``manage.py`` utility:

.. code-block:: bash

   $ python manage.py generate_profiles

Optional Arguments
~~~~~~~~~~~~~~~~~~

- ``--skip-confirmation``:
  Skips the user confirmation prompt and proceeds directly to assigning users to audiences.

Example usage:

.. code-block:: bash

   $ python manage.py generate_profiles --skip-confirmation

Command Flow
~~~~~~~~~~~~

1. **Check Audience Generation**:
   The command prompts the user to confirm whether the ``generate_audiences`` command has been run. If this confirmation is not provided (or skipped using the ``--skip-confirmation`` flag), the command exits.

2. **Retrieve Related Users**:
   The command fetches users related to models detected in the ``User`` by foreign key or related relationships.

3. **Create User Profiles**:
   If a user does not already have an associated ``UserAnnouncementProfile``, the command creates one.

4. **Assign Audiences**:
   Audiences are mapped to users based on the related models, and new assignments are created if they do not already exist. This avoids duplicate assignments.


Settings Impact
~~~~~~~~~~~~~~~

This command depends on the previous execution of the ``generate_audiences`` command, which creates the necessary audiences. Make sure that step has been completed before running this command.

Example Output
~~~~~~~~~~~~~~

When running the command, the following example output might be displayed:

.. code-block:: text

   Ensure you've run the 'generate_audiences' command before proceeding.
   Have you already run 'generate_audiences'? (yes/no): yes
   All users have been assigned to existing audiences successfully.

If no related users are found or if audiences are missing, you would see:

.. code-block:: text

   No users found related to the provided models.
   No valid audiences found. Please run 'generate_audiences' first. Exiting...
