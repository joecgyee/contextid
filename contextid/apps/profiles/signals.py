import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import IdentityProfile

# Deletes file from filesystem when IdentityProfile object is deleted
@receiver(post_delete, sender=IdentityProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)

# Deletes old file from filesystem when a NEW image is uploaded
@receiver(pre_save, sender=IdentityProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = IdentityProfile.objects.get(pk=instance.pk).profile_pic
    except IdentityProfile.DoesNotExist:
        return False

    new_file = instance.profile_pic
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)