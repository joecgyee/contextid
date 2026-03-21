from django import forms
from django.forms import inlineformset_factory
from .models import IdentityProfile
from apps.attributes.models import ProfileAttribute

class ProfileAttributeForm(forms.ModelForm):
    class Meta:
        model = ProfileAttribute
        fields = ['key', 'value_type', 'value_string', 'value_int', 'value_bool', 'value_date', 'value_url']
        labels = {
            'key': 'Key',
            'value_type': 'Value type',
            'value_string': 'String',
            'value_int': 'Integer',
            'value_bool': 'Yes/No',
            'value_date': 'Date',
            'value_url': 'URL Link',
        }
        widgets = {
            'value_date': forms.DateInput(attrs={'type': 'date'}),
            'value_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }
        help_texts = {
            'key': 'e.g. Gender',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        key = cleaned_data.get('key')
        
        # Check if this form instance is part of a profile
        # self.instance.profile is provided by the inline formset
        profile = getattr(self.instance, 'profile', None)

        if profile and key:
            # Check for existing attributes with the same key, excluding the current one (if editing)
            duplicate_exists = ProfileAttribute.objects.filter(
                profile=profile, 
                key__iexact=key # Case-insensitive check is safer
            ).exclude(pk=self.instance.pk).exists()

            if duplicate_exists:
                raise forms.ValidationError(
                    f"The attribute '{key}' already exists for this profile. Please edit the existing one or use a different key."
                )
        
        return cleaned_data


# Create the formset
AttributeFormSet = inlineformset_factory(
    IdentityProfile,
    ProfileAttribute,
    form=ProfileAttributeForm,
    extra=1,           # Start with 1 empty row
    can_delete=True    # Allow removing rows
)