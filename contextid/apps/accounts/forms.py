from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean(self):
        """
        Hook into the global clean to move password validation errors 
        from the non-field errors or password2 to password1.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # If UserCreationForm's internal validation found issues, 
        # they might be in 'non_field_errors' or attached to the wrong field.
        # We let the default validators run, then we ensure the UI is clean.
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields didn't match.")
            
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes
        for field_name in self.fields:
            field = self.fields[field_name]
            css_classes = "form-control"
            if self.errors.get(field_name):
                css_classes += " is-invalid"
            field.widget.attrs.update({'class': css_classes})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Try to find user by email if input looks like email
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                    self.cleaned_data['username'] = username
                except User.DoesNotExist:
                    raise ValidationError("No account found with this email address or username.")
        
        return super().clean()
