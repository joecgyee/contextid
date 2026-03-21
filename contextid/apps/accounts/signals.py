from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        # Look for the 'Users' group we created in the migration
        user_group = Group.objects.filter(name='Users').first()
        if user_group:
            instance.groups.add(user_group)