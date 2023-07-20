from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        field_classes = {}


class CustomUserChangePersonalDataForm(UserChangeForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    about_me = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'about_me')
        
