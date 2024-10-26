Examples
========

This section provides examples on how to handle various conditions in your project using ``dj-announcement-api``.

Assigning New Users to Audiences
--------------------------------

To automatically assign new registered users to specific audiences, `dj-announcement-api` provides several methods. You can use the management commands (``generate_audiences`` and ``generate_profiles``) to assign related users to their appropriate audiences. However, for real-time assignment of new users, automating this within models, serializers, or signals may be more efficient. Below are three recommended approaches for automatic assignment, along with instructions on command usage.

Method 1: Using the Model's `save` Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this approach, user-audience assignments are handled within the model's `save` method of the related model. This method can check if an instance is newly created and, if so, ensures that an `AnnouncementProfile` is generated automatically.

Steps:
1. Check for the audience corresponding to the model's verbose name, creating it if necessary.
2. Create an `AnnouncementProfile` for the new user associated with the audience.

.. code-block:: python

    from django.db import models
    from django_announcement.models import Audience, UserAnnouncementProfile


    class RelatedUserModel(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
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
                profile, _ = UserAnnouncementProfile.objects.get_or_create(user=self.user)
                profile.audiences.add(audience)
                profile.save()

Using this method ensures that each time a user instance is created, audience assignment occurs immediately.

Method 2: In the Serializer's `create` Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a more API-focused approach, handle audience assignments directly in the serializer's `create` method. This is ideal when user creation is managed through API endpoints.

.. code-block:: python

    from rest_framework import serializers
    from django_announcement.models import Audience, UserAnnouncementProfile


    class RelatedUserModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = RelatedUserModel
            fields = "__all__"

        def create(self, validated_data):
            instance = super().create(validated_data)

            # Fetch or create the audience
            audience, _ = Audience.objects.get_or_create(
                name=instance._meta.verbose_name.title()
            )

            # Assign the user to the audience
            profile, _ = UserAnnouncementProfile.objects.get_or_create(user=instance.user)
            profile.audiences.add(audience)
            profile.save()

            return instance

This approach is best for API-based workflows where user creation is handled via serializers.

Method 3: Using Signals
~~~~~~~~~~~~~~~~~~~~~~~

Signals allow handling audience assignments whenever a new user instance is created, keeping assignment logic separate from models and serializers.

Steps:
1. Create a post-save signal for the user-related model.
2. In the signal, retrieve or create the appropriate audience and announcement profile.

.. code-block:: python

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
            profile, _ = UserAnnouncementProfile.objects.get_or_create(user=instance.user)
            profile.audiences.add(audience)
            profile.save()

This approach enhances maintainability, particularly when user creation might occur in multiple parts of the codebase.

Using Management Commands for Batch Assignment
----------------------------------------------

If new roles or related models are added and require new audience creation, you can use the management commands:

1. Run ``generate_audiences`` to create audiences based on related models if they don't already exist.
2. Run ``generate_profiles`` to assign users to these audiences in bulk.

These commands are useful for batch operations and can be combined with the methods above to automatically assign audiences to new users as they are created.

Conclusion
----------

For automating audience assignments to new users, choose the approach that best suits your workflow:

- **Model save method** for tightly coupled functionality.
- **Serializer `create` method** for API-driven workflows.
- **Signals** for separation of concerns and modularity.
- **Management commands** for batch assignment and new role or audience generation.
