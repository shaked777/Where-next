from django.db.models.signals import post_save
from .models import Traveler
from django.contrib.auth.models import User, Group
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Post-create user signal that create profile with courrent user."""
    if created:
        Traveler.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Post-create user signal that save the profile from create_profile to the courrent user."""
    instance.traveler.save()

@receiver(post_save, sender=User)
def add_user_to_public_group(sender, instance, created, **kwargs):
    """Post-create user signal that adds the user to everyone group."""
    try:
        if created:
            instance.groups.add(Group.objects.get(name='travelers'))
    except Group.DoesNotExist:
        pass

