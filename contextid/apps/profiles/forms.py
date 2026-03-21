from django import forms
from django.core.exceptions import ValidationError
from .models import *

class IdentityProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Pop the user out of the kwargs so super() doesn't get confused
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = IdentityProfile
        fields = ['context', 'display_name', 'profile_pic', 'is_public']
        
        labels = {
            'context': 'Context',
            'display_name': 'Name',
            'profile_pic': 'Profile Picture',
            'is_public': 'Public',
        }
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'display_name': 'how you want to be seen, e.g., Dr. Smith',
            'profile_pic': 'maximum file size: 5MB',
            'is_public': 'make this profile visible to everyone.',
        }

    def clean(self):
            cleaned_data = super().clean()
            context = cleaned_data.get('context')

            # Check if this user already has a profile for this context
            if self.user and context:
                exists = IdentityProfile.objects.filter(
                    user=self.user, 
                    context=context
                ).exists()
                
                if exists:
                    # Add the error specifically to the 'context' field
                    self.add_error('context', "You already have a profile for this context.")
            
            return cleaned_data

    def clean_profile_pic(self):
        pic = self.cleaned_data.get('profile_pic')
        if pic:
            # 5MB limit
            if pic.size > 5 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 5MB )")
        return pic