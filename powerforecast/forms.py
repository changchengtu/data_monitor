from django import forms as f
from django.forms.widgets import TextInput
from powerforecast.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail

class ContactForm(f.ModelForm):
    first_name = f.CharField(
        label='', 
        error_messages={'required': 'please tell us who you are :)'},
        widget=f.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = f.EmailField(
        label='', 
        error_messages={'required': 'please let us contact you :)',
                         'invalid': 'please enter a valid email'},
        widget=f.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    class Meta:
        model = User
        fields = ['first_name', 'email']
    

class UserForm(f.Form):
    username = f.CharField(
        label = '',
        widget=f.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = f.CharField(
        label = '',
        widget=f.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    class Meta:
        model = User
        fields = ['username', 'password']

    # def clean(self):
    #     if (self.cleaned_data.get('email') != self.cleaned_data.get('confirm_email')):
    #         raise ValidationError("Email addresses must match.")
    #     self._errors['title'] = ['Invalid date given.']

    #     return self.cleaned_data