from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'university_email', 'username', 'password1', 'password2']
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('university_email')
        if email:
            valid_domains = ['fdu.edu', 'student.fdu.edu']
            if not any(email.endswith(domain) for domain in valid_domains):
                self.add_error('university_email', 'The email must end with @fdu.edu or @student.fdu.edu')
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='University Email')
