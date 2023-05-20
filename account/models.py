from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from .managers import UserManager


def _get_profile_image_filepath(self, *args):
    return f'user_images/{self.pk}/profile_image.jpg'


def _get_default_profile_image():
    return 'default_profile_image.jpg'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'электронная почта',
        unique=True)
    first_name = models.CharField(
        'имя',
        max_length=150)
    last_name = models.CharField(
        'фамилия',
        max_length=150)
    telegram_username = models.CharField(
        'имя пользователя телеграм',
        max_length=32, null=True, blank=True,
        validators=[MinLengthValidator(5)])
    image = models.ImageField(
        'изображение',
        upload_to=_get_profile_image_filepath,
        default=_get_default_profile_image,
        null=True, blank=True)
    created_at = models.DateTimeField(
        'дата создания',
        auto_now_add=True)
    last_login = models.DateTimeField(
        'дата последнего входа',
        auto_now=True)
    password_updated_at = models.DateTimeField(
        'дата последнего обновления пароля',
        auto_now_add=True)
    is_admin = models.BooleanField(
        'статус администратора',
        default=False)
    is_staff = models.BooleanField(
        'статус персонала',
        default=False)
    is_email_verified = models.BooleanField(
        'статус подтверждения электронной почты',
        default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def clean(self):
        errors = {}
        if self.first_name and self.first_name[0].islower():
            errors[
                'first_name'] = 'Имя не должно начинаться с маленькой буквы.'
        if self.last_name and self.last_name[0].islower():
            errors[
                'last_name'] = 'Фамилия не должна начинаться с маленькой буквы.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
