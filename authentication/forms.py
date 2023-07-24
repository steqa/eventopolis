from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=260)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        field_classes = {}


class UserPersonalDataChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    about_me = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'about_me')


class UserEmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': {
            'new_email2': 'Новый адрес электронной почты и повтор '
                          'нового адреса электронной почты не совпадают.'
        },
        'not_changed': {
            'new_email1': 'Адрес электронной почты совпадает с тем, '
                          'который уже определен.'
        },
        'email_exists': {
            'new_email1': 'Пользователь с таким адресом '
                          'электронной почты уже существует.'
        }
    }

    new_email1 = forms.EmailField(max_length=260)
    new_email2 = forms.EmailField(max_length=260)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEmailChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2 and old_email:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch'
                )
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed'
                )
            user = User.objects.filter(email=new_email1).exists()
            if user:
                raise forms.ValidationError(
                    self.error_messages['email_exists'],
                    code='email_exists'
                )
