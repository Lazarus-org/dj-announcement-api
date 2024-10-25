# Welcome to dj-announcement-api Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-announcement-api)](https://github.com/lazarus-org/dj-announcement-api/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-announcement-api)](https://pypi.org/project/dj-announcement-api/)
[![Documentation](https://img.shields.io/readthedocs/dj-announcement-api)](https://dj-announcement-api.readthedocs.io/en/latest/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-announcement-api)](https://pypi.org/project/dj-announcement-api/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-announcement-api)](https://pypi.org/project/dj-announcement-api/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-announcement-api)](https://github.com/lazarus-org/dj-announcement-api/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-announcement-api)](https://github.com/lazarus-org/dj-announcement-api/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-announcement-api)](https://github.com/lazarus-org/dj-announcement-api)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-announcement-api/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-announcement-api)

[`dj-announcement-api`](https://github.com/lazarus-org/dj-announcement-api/) is a versatile Django package developed by Lazarus to simplify the management and distribution of announcements via a robust API.

The package allows users to create and manage detailed, categorized announcements, target specific audiences, and schedule announcements with customizable publication and expiration dates.
It offers flexibility, scalability, and performance optimizations, making it ideal for dynamic needs in modern Django applications.

## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2
- Django REST Framework >= 3.14

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[API Guide](#api-guide)**: Detailed information on available APIs and endpoints.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[Examples](#examples)**: Examples of how to configure some key features.
- **[Settings](#settings)**: Configuration options and settings you can customize.


---

# Quick Start

This section provides a fast and easy guide to getting the `dj-announcement-api` package up and running in your Django project. Follow the steps below to quickly set up the package and start using it.

### 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-announcement-api
```
**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-announcement-api
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-announcement-api
```

The package requires ``djangorestframework`` for API support. If it's not already installed in your project, you can install it using one of the above methods:

**Using pip:**

```bash
$ pip install djangorestframework
```

### 2. Add to Installed Apps

After installing the necessary packages, ensure that both `rest_framework` and `django_announcement` are added to the `INSTALLED_APPS` in your Django ``settings.py`` file:

```python
INSTALLED_APPS = [
   # ...
   "rest_framework",  # Required for API support

   "django_announcement",
   # ...
]
```

### 3. (Optional) Configure API Filters

To enable filtering of announcements through the API, install ``django-filter``, include ``django_filters`` in your ``INSTALLED_APPS`` and configure the filter settings.

Install ``django-filter`` using one of the above methods:

**Using pip:**

```bash
$ pip install django-filter
```

Add `django_filters` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
   # ...
   "django_filters",
   # ...
]
```

Then, set the filter class configuration in your ``settings.py``:

```python
DJANGO_announcement_API_FILTERSET_CLASS = (
   "django_announcement.api.filters.announcement_filter.AnnouncementFilter"
)
```

You can also define your custom `FilterClass` and reference it in here if needed. This allows you to customize the filtering behavior according to your requirements.


### 4. Apply Migrations

Run the following command to apply the necessary migrations:

```bash
$ python manage.py migrate
```

### 5. Add Announcement API URLs

Include the announcement API routes in your project’s `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
   # ...
   path("announcement/", include("django_announcement.api.routers")),
   # ...
]
```

### 6. Generate Audiences and Profiles

After setting up the package and applying the migrations, run the management commands to generate the necessary audiences based on user related models and generate announcement profiles for users to assign audience to them.

First, generate the audiences using the ``generate_audiences`` command:

```shell

$ python manage.py generate_audiences
```

Then, assign users to these audiences by running the ``generate_profiles`` command:

```shell
$ python manage.py generate_profiles
```

### 7. Create Announcements via Django Admin

Now, you can create announcements using the Django admin interface.

- Log in to the Django admin site.
- Navigate to the **Announcements** section.
- Click **Add Announcement** to create a new announcement, filling out the required fields such as title, content and category.
- Optionally, select the target audiences and attach files if needed.

Once saved, your announcements will be available to the users assigned to the relevant audiences.


### 8. Verify Announcements

Once announcements are created, they can be viewed through the API endpoints. To test and verify the creation, make a request to the relevant endpoint, for example:

```bash
curl -X GET http://localhost:8000/announcement/annoucements/
```

This will return a list of announcements created in the admin.

---

With the setup complete, the ``dj-announcement-api`` is ready for use in your project. For further customizations and settings, refer to the [API Guide](#api-guide) and [Settings](#settings) sections.

----

# API Guide

This section provides a detailed overview of the Django Announcement API, allowing users to manage announcements efficiently. The API exposes two main endpoints:


## Announcements API

The ``announcement/announcements/`` endpoint provides the following features:

- **List active announcements**:

  Fetches all active announcements for the authenticated user (all announcements for admin users). Controlled by the ``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST`` setting.

- **Retrieve an announcement**:

  Retrieves a specific active announcement by its ID. Controlled by the ``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE`` setting.

---

## Example Responses

Here are some examples of responses for each action:


**List announcements with full details**:

```text
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
```

If the ``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS`` setting is ``True``, this detailed response will be returned for all users.

**List announcements with simplified data**:

```text
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
```

This response is returned when ``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS`` is set to ``False``. Admins always see full details.


> **Note:**
>
> you can exclude Any fields with empty value in the response output by adding this config in your ``settings.py``:

```python
DJANGO_ANNOUNCEMENT_SERIALIZER_EXCLUDE_EMPTY_FIELDS = True
```

---

## Throttling

The API includes a built-in throttling mechanism that limits the number of requests a user can make based on their role. You can customize these throttle limits in the settings file.

To specify the throttle rates for authenticated users and staff members, add the following in your settings:

```ini
DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE = "100/day"
DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE = "60/minute"
```

These settings limit the number of requests users can make within a given timeframe.

**Note:** You can define custom throttle classes and reference them in your settings.

---

## Filtering, Ordering, and Search

The API supports filtering, ordering, and searching of announcements. Filter Class can be applied optionally, allowing users to narrow down results.

Options include:

- **Filtering**: By default filtering feature is not included, If you want to use this, you need to add ``django_filters`` to your `INSTALLED_APPS` and provide the path to the ``AnnouncementFilter`` class (``"django_announcement.api.filters.announcement_filter.AnnouncementFilter"``). Alternatively, you can use a custom filter class if needed.

  - **Note**: for more clarification, refer to the `DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS` in :doc:`Settings <settings>` section.

- **Ordering**: Results can be ordered by fields such as ``id``, ``timestamp``, or ``public``.

- **Search**: You can search fields like ``verb`` and ``description``.

These fields can be customized by adjusting the related configurations in your Django settings.

---

## Pagination

The API supports limit-offset pagination, with configurable minimum, maximum, and default page size limits. This controls the number of results returned per page.

---

## Permissions

The base permission for all endpoints is ``IsAuthenticated``, meaning users must be logged in to access the API. You can extend this by creating custom permission classes to implement more specific access control.

For instance, you can allow only specific user roles to perform certain actions.

---

## Parser Classes

The API supports multiple parser classes that control how data is processed. The default parsers include:

- ``JSONParser``
- ``MultiPartParser``
- ``FormParser``

You can modify parser classes by updating the API settings to include additional parsers or customize the existing ones to suit your project.

----

Each feature can be configured through the Django settings file. For further details, refer to the [Settings](#settings) section.

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of the Django admin panels for managing announcements, announcement categories, audiences, user announcement profile and Manager methods for handling announcements.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your Django settings. Otherwise, Django may raise the following error during checks:

```shell
ERRORS:
<class 'django_announcement.admin.announcement_profile.UserAnnouncementProfileAdmin'>:
(admin.E039) An admin for model "User" has to be registered to be referenced by UserAnnouncementProfileAdmin.autocomplete_fields.
```

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class instance

```python
DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS = "path.to.your.custom.site"
```

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
  site_header = "Custom Admin"
  site_title = "Custom Admin Portal"
  index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-announcement-api` to use your custom admin site for its Admin interface, preventing any errors and ensuring a smooth integration with the custom admin interface.


## Announcements Admin Panel

The ``AnnouncementAdmin`` class provides a comprehensive admin interface for managing announcements in the Django admin panel. The features and functionality are described below:


### Inline Admin Interfaces

The ``AnnouncementAdmin`` panel includes two inline admin interfaces that allow admins to view and manage related models directly from the announcement page:

- ``AudienceInline``:

  Displays and manages the audiences associated with each announcement. Admins can view or add audience directly within the announcement details page.


### List Display

The list view for announcements includes the following fields:

- ``ID``: The unique identifier for each announcement.
- ``Title``: The announcement title or a summary.
- ``Category``: The category of the announcement.
- ``Created at``: Creation time of the announcement.
- ``Expires at``: Expiration time of the announcement.

This view helps admins get a quick overview of the announcements and their current status.

### Filtering

Admins can filter the list of announcements based on the following fields:

- ``created_at``: Filter by the creation time of the announcement.
- ``updated_at``: Filter by the time that the announcement last updated.
- ``category``: Filter by announcement category.

These filters make it easier to find specific announcements or groups of announcements based on category or time.

### Search Functionality

Admins can search for announcements using the following fields:

- ``ID``: The unique identifier of the announcement.
- ``Title``: The Title of the announcement.
- ``Content``: The content of the announcement.
- ``Audience Name``: The name of the audience associated with the announcement.

This search functionality enables quick access to specific announcements by key identifiers.

### Pagination

The admin list view displays **10 announcements per page** by default. This can help improve load times and make it easier for admins to manage large lists of announcements.

### Permissions Configuration

The admin permissions for ``add``, ``change``, and ``delete`` actions and also ``module`` permission can be controlled through the following Django settings:

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION``: Controls whether the "add" action is available in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION``: Controls whether the "change" action is allowed in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION``: Controls whether the "delete" action is available in the Announcements, Audiences and UserAnnouncementProfile Admin and so on. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION``: Determines whether a user has access to the admin management module, including all its features and functionality. Defaults to ``True``.


The admin inline permissions for ``add``, ``change``, and ``delete`` actions can be controlled through the following Django settings:

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION``: Controls whether the "add" action is available in the AudienceInline and UserAudienceInline Admin. Defaults to ``True``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION``: Controls whether the "change" action is allowed in the AudienceInline and UserAudienceInline Admin. Defaults to ``False``.

- ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION``: Controls whether the "delete" action is available in the AudienceInline and UserAudienceInline Admin. Defaults to ``True``.

---

## Announcement Categories Admin Panel

The ``AnnouncementCategoryAdmin`` class provides an admin interface for managing announcement categories. Key features include:

### List Display

The list view for categories includes the following fields:

- ``ID``: The unique identifier of the category.
- ``Name``: The name of the category.
- ``Created at``: The time the category was created.
- ``Updated at``: The time the category was last updated.

This allows for a quick overview of available announcement categories.

### Filtering

Admins can filter categories by:

- ``Created at``: Filter by the creation time of the category.
- ``Updated at``: Filter by the time the category was last updated.

### Search Functionality

Admins can search for categories using:

- ``Name``: The name of the category.
- ``Description``: The description of the category.

### Fieldsets

The admin panel displays the following fields when editing a category:

- ``ID``: The unique identifier of the category.
- ``Name``: The name of the category.
- ``Description``: A description of the category.

---

## Audiences Admin Panel

The ``AudienceAdmin`` class provides a user-friendly admin interface for managing audiences in the Django admin panel. Key features are described below:

### Inline Admin Interfaces

The ``AudienceAdmin`` panel includes inline admin interfaces for managing related models:

- ``UserAudienceInline``:

  Allows admins to view and manage users associated with a specific audience directly within the audience details page.

### List Display

The list view for audiences includes the following fields:

- ``ID``: The unique identifier for each audience.
- ``Name``: The name of the audience.
- ``Created at``: The creation time of the audience.
- ``Updated at``: A time that the audience was last updated.

This display helps admins quickly view and manage different audience groups.

### Filtering

Admins can filter the list of audiences based on the following fields:

- ``created_at``: Filter by the creation date of the audience.
- ``created_at``: Filter by the last updated date of the audience.

### Search Functionality

Admins can search for audiences using the following fields:

- ``ID``: The unique identifier of the audience.
- ``Name``: The name of the audience.
- ``Description``: The description of the audience.

### Pagination

The admin list view shows **10 audiences per page** by default to improve load times and manageability.

---

## User Announcement Profiles Admin Panel

The ``UserAnnouncementProfileAdmin`` class allows admins to manage the relationship between users and their assigned audiences.

### Inline Admin Interfaces

The admin interface includes the following inline:

- ``UserAudienceInline``:

  Allows admins to view or manage the audiences assigned to a specific user from the user announcement profile page.

### List Display

The list view for user profiles includes the following fields:

- ``ID``: The unique identifier for each profile.
- ``User``: The associated user for the profile.
- ``Created at``: The creation time of the profile.
- ``Updated at``: The last updated time of the profile.

This helps admins manage user profiles and their audience relationships efficiently.

### Filtering

Admins can filter user profiles by the following fields:

- ``created_at``: Filter by the creation date of the profile.
- ``created_at``: Filter by the last updated date of the audience.

### Search Functionality

Admins can search for user profiles using the following fields:

- ``ID``: The unique identifier for each profile.
- ``User ID``: The Unique identifier of the associated user.
- ``User name``: The username of the associated user.
- ``Audience name``: The name of the assigned audience.

### Pagination

The admin list view shows **10 user profiles per page** by default to optimize load times.

---

## Audience Announcements Admin Panel

The ``AudienceAnnouncementAdmin`` class provides an interface to manage the relationship between audiences and announcements.

### List Display

The list view includes the following fields:

- ``ID``: The unique identifier of the AudienceAnnouncement.
- ``Audience``: The name of the audience.
- ``Announcement``: The associated announcement title.
- ``Created at``: The time the association was created.

Filtering and search options help manage and explore audience-announcement pairs.

### Filtering

Admins can filter categories by:

- ``Created at``: Filter by the creation time of the AudienceAnnouncement.
- ``Updated at``: Filter by the time the category was last updated.

### Search Functionality

Admins can search for audience-announcement relations by:

- ``ID``: The unique identifier of the audience-announcement.
- ``Announcement Title``: The title of the announcement.
- ``Audience Name``: The name of the audience.


## User Audience Admin Panel

The ``UserAudienceAdmin`` class provides an admin interface for managing user-audience relationships.

### List Display

The list view includes the following fields:

- ``ID``: The unique identifier for each user-audience.
- ``User Announcement Profile``: The user profile linked to the audience.
- ``Audience``: The audience assigned to the user.
- ``Created at``: The time the user was assigned to the audience.

This makes managing user-audience relations straightforward.

### Search Functionality

Admins can search for user-audience relations by:

- ``ID``: The unique identifier for each user-audience.
- ``User Name``: The username of the associated user.
- ``User ID``: The ID of the user.
- ``Audience Name``: The name of the audience.

---

## AnnouncementDataAccessLayer (Manager)

The ``django_announcement`` app provides a Manager Class ``AnnouncementDataAccessLayer`` with various methods to interact with announcements in different contexts. Users typically use `Announcement.objects.all()` to retrieve announcements, but other methods are available for querying specific subsets of announcements. Below is an overview of the available methods:


### Return All Announcements

The ``all`` method retrieves all announcements from the database.

**Method Signature**

```python
from django_announcement.models import Announcement

Announcement.objects.all()
```

**Returns:**

- A ``QuerySet`` of all announcements in the system.

**Example Usage:**

To retrieve all announcements:

```python
from django_announcement.models import Announcement

all_announcements = Announcement.objects.all()
```

### Return Active Announcements

The ``active`` method retrieves only the announcements that are currently active (published and not expired).

**Method Signature**

```python
from django_announcement.models import Announcement

Announcement.objects.active()
```

**Returns:**

- A ``QuerySet`` of active announcements.

**Example Usage:**

To retrieve all active announcements:

```python
from django_announcement.models import Announcement

active_announcements = Announcement.objects.active()
```

### Return Upcoming Announcements

The ``upcoming`` method retrieves announcements that are scheduled to be published in the future.

**Method Signature**

```python

from django_announcement.models import Announcement

Announcement.objects.upcoming()
```

**Returns:**

- A ``QuerySet`` of announcements scheduled for future publication.

**Example Usage:**

To retrieve all upcoming announcements:

```python
from django_announcement.models import Announcement

upcoming_announcements = Announcement.objects.upcoming()
```

### Return Expired Announcements

The ``expired`` method retrieves announcements that have already expired.

**Method Signature**

```python

from django_announcement.models import Announcement

Announcement.objects.expired()
```

**Returns:**

- A ``QuerySet`` of expired announcements.

**Example Usage:**

To retrieve all expired announcements:

```python
from django_announcement.models import Announcement

expired_announcements = Announcement.objects.expired()
```

### Retrieve Announcements by Audience

The ``get_by_audience`` method retrieves announcements targeted at specific audience(s).

**Method Signature**

```python

from django_announcement.models import Announcement, Audience

audiences = Audience.objects.filter(name__icontains="manager")
Announcement.objects.get_by_audience(audiences)
```

**Arguments:**

- **audiences** (``Audiences``):
  An audience instance, audience ID, or an iterable of audience instances to filter announcements by.

**Returns:**

- A ``QuerySet`` of announcements for the given audience(s).

**Example Usage:**

To retrieve announcements for a specific audience:

```python
from django_announcement.models import Announcement, Audience

specific_audience = Audience.objects.get(id=1)
audience_announcements = Announcement.objects.get_by_audience(specific_audience)
```

### Retrieve Announcements by Category

The ``get_by_category`` method retrieves announcements filtered by specific category(s).

**Method Signature**

```python
from django_announcement.models import Announcement, AnnouncementCategory

categories = AnnouncementCategory.objects.filter(id__in=[1, 2])
Announcement.objects.get_by_category(categories)
```

**Arguments:**

- **categories** (``Categories``):
  A category instance, category ID, or an iterable of category instances to filter announcements by.

**Returns:**

- A ``QuerySet`` of announcements for the given category(s).

**Example Usage:**

To retrieve announcements for a specific category:

```python
from django_announcement.models import Announcement, AnnouncementCategory

specific_category = AnnouncementCategory.objects.get(id=2)
category_announcements = Announcement.objects.get_by_category(specific_category)
```

## generate_audiences Command

The ``generate_audiences`` command dynamically creates audiences based on models related to the ``User``. It allows filtering out specific apps and models through configuration settings, and includes an optional user confirmation step before proceeding.

### Command Overview

This command scans for related models in the ``User`` (excluding those defined in the settings), confirms the list of models with the user, and creates audiences if they don't already exist. It is useful for dynamically creating target audiences for announcements based on your application's data models.

### Settings

This command is influenced by two key settings:

- ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS``:
  A list of app labels to exclude from the audience generation process.

- ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS``:
  A list of model names to exclude from the audience generation process.

These settings allow for fine-grained control over which models are considered for audience creation.

### Usage

The command can be run using Django's ``manage.py`` utility:

```bash
$ python manage.py generate_audiences
```

### Optional Arguments

- ``--skip-confirmation``:
  Skips the user confirmation prompt and proceeds directly to creating audiences.

Example usage:

```bash
$ python manage.py generate_audiences --skip-confirmation
```

### Command Flow

1. **Retrieve Related Models**:
   The command first retrieves all models related to the ``User`` by checking the relationships. It filters out any models and apps specified in the ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS`` and ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS`` settings.

2. **Prompt for Confirmation**:
   The command lists the related models found and asks for confirmation from the user to proceed. If the ``--skip-confirmation`` flag is provided, this step is bypassed.

3. **Create Audiences**:
   For each related model that doesn't already have a corresponding audience, the command creates a new audience and saves it in the database. It checks the existing audiences by their name to avoid duplications.

### Example Output

When running the command, the following example output might be displayed:

```text
The following related models were found:
1. User Profile
2. Organization

Are these the correct target models? Type 'y' to proceed or 'n' to modify settings: y
Created audience: User Profile
Created audience: Organization
Finished creating audiences!
```

If no new audiences are needed, you would see:

```text
No new audiences needed to be created.
```

---

## generate_profiles Command

The ``generate_profiles`` command assigns users to dynamically created audiences using the ``UserAnnouncementProfile`` model. It ensures that users are correctly associated with audiences based on user-related models in the database. This command should be run after the ``generate_audiences`` command to link users to the relevant audiences.

### Command Overview

This command checks if the audience generation has been completed, then proceeds to create user profiles if they do not already exist. It builds and assigns audience-user relationships dynamically, based on the user-related models detected in the system.

### Usage

The command can be run using Django's ``manage.py`` utility:

```bash
$ python manage.py generate_profiles
```

### Optional Arguments

- ``--skip-confirmation``:
  Skips the user confirmation prompt and proceeds directly to assigning users to audiences.

Example usage:

```bash
$ python manage.py generate_profiles --skip-confirmation
```

### Command Flow

1. **Check Audience Generation**:
   The command prompts the user to confirm whether the ``generate_audiences`` command has been run. If this confirmation is not provided (or skipped using the ``--skip-confirmation`` flag), the command exits.

2. **Retrieve Related Users**:
   The command fetches users related to models detected in the ``User`` by foreign key or related relationships.

3. **Create User Profiles**:
   If a user does not already have an associated ``UserAnnouncementProfile``, the command creates one.

4. **Assign Audiences**:
   Audiences are mapped to users based on the related models, and new assignments are created if they do not already exist. This avoids duplicate assignments.

### Settings Impact

This command depends on the previous execution of the ``generate_audiences`` command, which creates the necessary audiences. Make sure that step has been completed before running this command.

### Example Output

When running the command, the following example output might be displayed:

```text
Ensure you've run the 'generate_audiences' command before proceeding.
Have you already run 'generate_audiences'? (yes/no): yes
All users have been assigned to existing audiences successfully.
```

If no related users are found or if audiences are missing, you would see:

```text
No users found related to the provided models.
No valid audiences found. Please run 'generate_audiences' first. Exiting...
```

----

# Examples

This section provides examples on how to handle various conditions in your project using ``dj-announcement-api``.

## Assigning New Users to Audiences

To automatically assign new registered users to specific audiences, `dj-announcement-api` provides several methods. You can use the management commands (``generate_audiences`` and ``generate_profiles``) to assign related users to their appropriate audiences. However, for real-time assignment of new users, automating this within models, serializers, or signals may be more efficient. Below are three recommended approaches for automatic assignment, along with instructions on command usage.

### Method 1: Using the Model's `save` Method


In this approach, user-audience assignments are handled within the model's `save` method of the related model. This method can check if an instance is newly created and, if so, ensures that an `AnnouncementProfile` is generated automatically.

Steps:
1. Check for the audience corresponding to the model's verbose name, creating it if necessary.
2. Create an `AnnouncementProfile` for the new user associated with the audience.

```python
from django.db import models
from django_announcement.models import Audience, UserAnnouncementProfile

class RelatedUserModel(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    # additional fields

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Retrieve or create the audience based on model name
            audience, _ = Audience.objects.get_or_create(
                name=self._meta.verbose_name.title()
            )

            # Create the announcement profile for this user
            profile, _ = UserAnnouncementProfile.objects.get_or_create(
                user=self.user
            )
            profile.audiences.add(audience)
            profile.save()
```

Using this method ensures that each time a user instance is created, audience assignment occurs immediately.

### Method 2: In the Serializer's `create` Method

For a more API-focused approach, handle audience assignments directly in the serializer's `create` method. This is ideal when user creation is managed through API endpoints.

```python

from rest_framework import serializers
from django_announcement.models import Audience, UserAnnouncementProfile

class RelatedUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedUserModel
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)

        # Fetch or create the audience
        audience, _ = Audience.objects.get_or_create(
            name=instance._meta.verbose_name.title()
        )

        # Assign the user to the audience
        profile, _ = UserAnnouncementProfile.objects.get_or_create(
            user=instance.user
        )
        profile.audiences.add(audience)
        profile.save()

        return instance
```

This approach is best for API-based workflows where user creation is handled via serializers.

### Method 3: Using Signals

Signals allow handling audience assignments whenever a new user instance is created, keeping assignment logic separate from models and serializers.

Steps:
1. Create a post-save signal for the user-related model.
2. In the signal, retrieve or create the appropriate audience and announcement profile.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_announcement.models import Audience, UserAnnouncementProfile
from .models import RelatedUserModel

@receiver(post_save, sender=RelatedUserModel)
def assign_audience_to_new_user(sender, instance, created, **kwargs):
    if created:
        # Retrieve or create audience
        audience, _ = Audience.objects.get_or_create(
            name=instance._meta.verbose_name.title()
        )

        # Assign user to the audience
        profile, _ = UserAnnouncementProfile.objects.get_or_create(
            user=instance.user
        )
        profile.audiences.add(audience)
        profile.save()
```

This approach enhances maintainability, particularly when user creation might occur in multiple parts of the codebase.

## Using Management Commands for Batch Assignment

If new roles or related models are added and require new audience creation, you can use the management commands:

1. Run ``generate_audiences`` to create audiences based on related models if they don't already exist.
2. Run ``generate_profiles`` to assign users to these audiences in bulk.

These commands are useful for batch operations and can be combined with the methods above to automatically assign audiences to new users as they are created.

## Conclusion

For automating audience assignments to new users, choose the approach that best suits your workflow:

- **Model save method** for tightly coupled functionality.
- **Serializer `create` method** for API-driven workflows.
- **Signals** for separation of concerns and modularity.
- **Management commands** for batch assignment and new role or audience generation.

----

# Settings

This section outlines the available settings for configuring the `dj-announcement-api` package. You can customize these settings in your Django project's `settings.py` file to tailor the behavior of the announcement system to your needs.

## Example Settings

Below is an example configuration with default values:

```python
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
```

## Settings Overview

Below is a detailed description of each setting, so you can better understand and tweak them to fit your project's needs.


### ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_ADD_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows adding new instances. Set this to ``False`` to disable Admin users to create new instances.


---

### ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_CHANGE_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows modifying existing instances. Set this to ``False`` to disable Admin users to edit instances.

---

### ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_DELETE_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin interface allows deleting instances. Set this to ``False`` to disable Admin users to delete instances.

---

### ``DJANGO_ANNOUNCEMENT_ADMIN_HAS_MODULE_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Determines whether a user has access to the admin management module, including all its features and functionality. Set this to ``False`` to hide the dj-announcement-api related admin.

---

### ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_ADD_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin inline interface allows adding new instances. Set this to ``False`` to disable Admin users to create new inline instances.


---

### ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_CHANGE_PERMISSION``

**Type**: ``bool``

**Default**: ``False``

**Description**: Controls whether the admin inline interface allows modifying existing instances. Set this to ``True`` to enable Admin users to edit inline instances.

---

### ``DJANGO_ANNOUNCEMENT_ADMIN_INLINE_HAS_DELETE_PERMISSION``

**Type**: ``bool``

**Default**: ``True``

**Description**: Controls whether the admin inline interface allows deleting instances. Set this to ``False`` to disable Admin users to delete inline instances.

---

### ``DJANGO_ANNOUNCEMENT_ADMIN_SITE_CLASS``

**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies A custom AdminSite class to apply on Admin interface. This allows for more customization on Admin interface, enabling you to apply your AdminSite class into `dj-announcement-api` Admin interface.

---

### ``DJANGO_ANNOUNCEMENT_SERIALIZER_INCLUDE_FULL_DETAILS``

**Type**: ``bool``

**Default**: ``False``

**Description**: When set to ``True``, API responses will include all announcement fields. By default, only essential fields are returned.

---

### ``DJANGO_ANNOUNCEMENT_SERIALIZER_EXCLUDE_EMPTY_FIELDS``

**Type**: ``bool``

**Default**: ``False``

**Description**: When set to ``True``, API responses will exclude any fields that does not have value.

---

### ``DJANGO_ANNOUNCEMENT_API_ALLOW_LIST``

**Type**: ``bool``

**Default**: ``True``

**Description**: Allows the listing of announcements via the API. Set to ``False`` to disable this feature.

---

### ``DJANGO_ANNOUNCEMENT_API_ALLOW_RETRIEVE``

**Type**: ``bool``

**Default**: ``True``

**Description**: Allows retrieving individual announcements via the API. Set to ``False`` to disable this feature.

---

### ``DJANGO_ANNOUNCEMENT_ATTACHMENT_VALIDATORS``

**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Allows specifying a list of additional validators for attachment files in announcements. Each validator should be passed as a Python path string, which can be dynamically loaded and applied to the attachment. For example, to add custom file size or file type validation, include paths to custom validator functions or classes.

----

### ``DJANGO_ANNOUNCEMENT_ATTACHMENT_UPLOAD_PATH``

**Type**: ``str``

**Default**: ``"announcement_attachments/"``

**Description**: Specifies the upload path for attachment files in announcements.

---

### ``DJANGO_ANNOUNCEMENT_AUTHENTICATED_USER_THROTTLE_RATE``

**Type**: ``str``

**Default**: ``"30/minute"``

**Description**: Sets the throttle rate (requests per minute, hour or day) for authenticated users in the API.

---

### ``DJANGO_ANNOUNCEMENT_STAFF_USER_THROTTLE_RATE``

**Type**: `str`

**Default**: `"100/minute"`

**Description**: Sets the throttle rate (requests per minute, hour or day) for staff (Admin) users in the API.

---

### ``DJANGO_ANNOUNCEMENT_API_THROTTLE_CLASS``

**Type**: ``str``

**Default**: ``"django_announcement.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"``

**Description**:  Specifies the throttle class used to limit API requests. Customize this or set it to ``None`` if no throttling is needed or want to use ``rest_framework`` `DEFAULT_THROTTLE_CLASSES`.

---

### ``DJANGO_ANNOUNCEMENT_API_PAGINATION_CLASS``

**Type**: ``str``

**Default**: ``"django_announcement.api.paginations.limit_offset_pagination.DefaultLimitOffSetPagination"``

**Description**: Defines the pagination class used in the API. Customize this if you prefer a different pagination style or set to ``None`` to disable pagination.

---

### ``DJANGO_ANNOUNCEMENT_API_EXTRA_PERMISSION_CLASS``

**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies an additional permission class to extend the base permission (``IsAuthenticated``) for the API. This allows for more fine-grained access control, enabling you to restrict API access to users with a specific permission, in addition to requiring authentication.

---

### ``DJANGO_ANNOUNCEMENT_API_PARSER_CLASSES``

**Type**: ``List[str]``

**Default**:

```python
DJANGO_ANNOUNCEMENT_API_PARSER_CLASSES = [
   "rest_framework.parsers.JSONParser",
   "rest_framework.parsers.MultiPartParser",
   "rest_framework.parsers.FormParser",
]
```

**Description**: Specifies the parsers used to handle API request data formats. You can modify this list to add your parsers or set ``None`` if no parser needed.

---

### ``DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS``

**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Specifies the filter class for API queries. If you want to use this, you need to **install** and add ``django_filters`` to your `INSTALLED_APPS` and provide the path to the ``AnnouncementFilter`` class (``"django_ANNOUNCEMENT.api.filters.announcement_filter.AnnouncementFilter"``). Alternatively, you can use a custom filter class if needed.

in your settings.py:

```python
INSTALLED_APPS = [
  # ...
  "django_filters",
  # ...
]
```

and then apply this setting:

```python
# apply in settings.py

DJANGO_ANNOUNCEMENT_API_FILTERSET_CLASS = (
  "django_announcement.api.filters.announcement_filter.AnnouncementFilter"
)
```
---

### ``DJANGO_ANNOUNCEMENT_API_ORDERING_FIELDS``

**Type**: ``List[str]``

**Default**: ``["id", "published_at", "expires_at", "created_at", "updated_at"]``

**Description**: Specifies the fields available for ordering in API queries, allowing the API responses to be sorted by these fields. you can see all available fields here

---

### ``DJANGO_ANNOUNCEMENT_API_SEARCH_FIELDS``

**Type**: ``List[str]``

**Default**: ``["title", "content", "category__name"]``

**Description**: Specifies the fields that are searchable in the API, allowing users to filter results based on these fields.

---

### ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS``

**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Specifies a list of app labels that should be excluded when running the `generate_audiences` command. If certain apps should not be considered for audience generation, list them here. For example:

```python

DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_APPS = ["finance", "store"]
```

This setting prevents the `generate_audiences` command from scanning the specified apps when creating dynamic audiences.

---

### ``DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS``

**Type**: ``list``

**Default**: ``[]`` (empty list)

**Description**: Specifies a list of model names that should be excluded when running the generate_audiences command. If certain models should not be included in the audience generation process, define them here. For example:

```python
DJANGO_ANNOUNCEMENT_GENERATE_AUDIENCES_EXCLUDE_MODELS = ["CustomModel", "AnotherModel"]
```

This setting allows fine-tuned control over which models are excluded from audience creation, even if their app is not fully excluded.

---

### All Available Fields

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

> **Note**:
> Exercise caution when modifying search and ordering fields. **Avoid** using foreign key or joined fields (``audience``, ``category``) directly in **search fields**, as this may result in errors. if you want to use them, you should access their fields like: ``category__name``.

----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-announcement-api`. Whether you're setting up for the first time or diving deep into API customization, this document covers essential steps, configurations, and use cases to help you make the most of the package. For more clear documentation, customization options, and updates, please refer to the official documentation on [Read the Docs](https://dj-announcement-api.readthedocs.io/).

### Final Notes:
- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python versions.
- **API Integration**: The package is designed for flexibility, allowing you to customize many features based on your application's needs.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for more details.

If you encounter any issues or have feedback, please reach out via our [GitHub Issues page](https://github.com/lazarus-org/dj-announcement-api/issues).
