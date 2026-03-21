from django.conf import settings
from django.db import models
from apps.contexts.models import Context

User = settings.AUTH_USER_MODEL

class IdentityProfile(models.Model):
    """
    One user can have multiple profiles,
    but only one per context.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="identity_profiles"
    )
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
        related_name="profiles"
    )

    display_name = models.CharField(max_length=150)
    profile_pic = models.ImageField(
        upload_to='profile_pics/%Y/%m/', 
        blank=True, 
        null=True
    )

    is_public = models.BooleanField(default=False) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "context")

    def __str__(self):
        return f"{self.user} - {self.context}'s Profile"
    
    @property
    def get_profile_pic_url(self):
        """
        Returns the profile picture URL if it exists, 
        otherwise returns the path to a default placeholder.
        """
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        
        return f"{settings.STATIC_URL}images/default-avatar.png"
