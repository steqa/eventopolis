import hashlib
import mimetypes
from string import ascii_letters, digits

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from .managers import UserManager


def _get_image_filepath(self, *args) -> str:
    return f'user_images/{self.pk}/profile_image.jpg'


def _get_default_image() -> str:
    return 'default_profile_image.jpg'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=260,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150
    )
    about_me = models.TextField(
        verbose_name='обо мне',
        max_length=150,
        null=True,
        blank=True
    )
    telegram_username = models.CharField(
        verbose_name='имя пользователя телеграм',
        validators=[MinLengthValidator(5)],
        max_length=32,
        null=True,
        blank=True
    )
    telegram_notifications = models.BooleanField(
        verbose_name='получать уведомления в телеграм',
        default=False
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=_get_image_filepath,
        default=_get_default_image
    )
    slug = models.SlugField(
        verbose_name='текстовый идентификатор страницы',
        validators=[MinLengthValidator(5)],
        max_length=32,
        unique=True,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='дата последнего входа',
        auto_now=True
    )
    password_updated_at = models.DateTimeField(
        verbose_name='дата последнего обновления пароля',
        auto_now_add=True
    )
    is_admin = models.BooleanField(
        verbose_name='статус администратора',
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name='статус персонала',
        default=False
    )
    is_email_verified = models.BooleanField(
        verbose_name='статус подтверждения электронной почты',
        default=False
    )

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

        if self.image:
            allowed_file_types = ('image/jpeg',)
            allowed_file_size = 1048576

            if self.image.size > allowed_file_size:
                error = 'Размер изображения не может превышать 1 МБ.'
                errors['image'] = error

            file_type, _ = mimetypes.guess_type(self.image.name)
            if file_type not in allowed_file_types:
                error = 'Доступные форматы изображения: JPG, JPEG.'
                errors['image'] = error

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
