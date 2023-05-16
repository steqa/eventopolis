from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from .managers import UserManager


def _get_profile_image_filepath(self, *args):
    return f'user_images/{self.pk}/profile_image.jpg'


def _get_default_profile_image():
    return 'default_profile_image.jpg'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    telegram_username = models.CharField(
        max_length=32, null=True, blank=True,
        validators=[MinLengthValidator(5)])
    image = models.ImageField(
        upload_to=_get_profile_image_filepath,
        default=_get_default_profile_image,
        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    password_updated_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
