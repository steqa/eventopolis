# Generated by Django 4.2 on 2023-06-03 12:41

import account.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('first_name', models.CharField(max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('telegram_username', models.CharField(blank=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='имя пользователя телеграм')),
                ('image', models.ImageField(blank=True, default=account.models._get_default_profile_image, null=True, upload_to=account.models._get_profile_image_filepath, verbose_name='изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='дата последнего входа')),
                ('password_updated_at', models.DateTimeField(auto_now_add=True, verbose_name='дата последнего обновления пароля')),
                ('is_admin', models.BooleanField(default=False, verbose_name='статус администратора')),
                ('is_staff', models.BooleanField(default=False, verbose_name='статус персонала')),
                ('is_email_verified', models.BooleanField(default=False, verbose_name='статус подтверждения электронной почты')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'db_table': 'auth_user',
            },
        ),
    ]
