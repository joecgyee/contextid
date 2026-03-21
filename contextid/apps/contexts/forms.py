from django import forms
from .models import *

class ContextForm(forms.ModelForm):
    class Meta:
        model = Context
        fields = ['name']
