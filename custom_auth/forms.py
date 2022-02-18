from django.utils.translation import gettext_lazy as _
from django.forms import Form
from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()

        
class CustomUserLoginForm(Form):

    username = forms.CharField(
        label=_('Email/Username'),
        max_length=150, 
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'email or username', 'class': 'input'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'input'}), 
        required=True
    )
