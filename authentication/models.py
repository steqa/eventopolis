import hashlib
from string import ascii_letters, digits

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
        max_length=260, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=150)
    last_name = models.CharField(
        'фамилия',
        max_length=150)
    about_me = models.TextField(
        'обо мне',
        max_length=150, null=True, blank=True)
    telegram_username = models.CharField(
        'имя пользователя телеграм',
        max_length=32, null=True, blank=True,
        validators=[MinLengthValidator(5)])
    telegram_notifications = models.BooleanField(
        'получать уведомления в телеграм',
        default=False)
    image = models.ImageField(
        'изображение',
        upload_to=_get_profile_image_filepath,
        default=_get_default_profile_image,
        null=True, blank=True)
    slug = models.SlugField(
        'текстовый идентификатор страницы',
        unique=True, blank=True, null=True, max_length=32,
        validators=[MinLengthValidator(5)])
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

        if self.first_name:
            if self.first_name[0].islower():
                error = 'Имя не должно начинаться с маленькой буквы.'
                errors['first_name'] = error

            if not self.first_name.isalpha():
                error = 'Имя может содержать только буквы.'
                errors['first_name'] = error

        if self.last_name:
            if self.last_name[0].islower():
                error = 'Фамилия не должна начинаться с маленькой буквы.'
                errors['last_name'] = error

            if not self.last_name.isalpha():
                error = 'Фамилия может содержать только буквы.'
                errors['last_name'] = error

        if self.telegram_username:
            allowed_chars = ascii_letters + digits + '_'
            if any(i not in allowed_chars for i in self.telegram_username):
                error = 'Имя пользователя телеграм должно состоять только из' \
                        ' латинских букв, цифр или знаков подчеркивания.'
                errors['telegram_username'] = error

        if self.slug:
            exists_user = User.objects.filter(slug=self.slug).first()
            if exists_user and exists_user.id != self.id:
                error = 'Пользователь с таким адресом страницы уже существует.'
                errors['slug'] = error

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            hasher = hashlib.sha256()
            hasher.update(self.email.encode())
            slug = hasher.hexdigest()[:15]
            while User.objects.filter(slug=slug).exists():
                hasher.update(slug.encode())
                slug = hasher.hexdigest()[:15]

            self.slug = slug
        return super().save(*args, **kwargs)
