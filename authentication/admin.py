from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'created_at', 'is_email_verified')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at', 'last_login',
                       'password_updated_at', 'preview_image')
    fieldsets = (
        (None,
         {'fields': (
             'id',
             'slug',
             'email',
             'password'
         )}),
        ('Персональная информация',
         {'fields': (
             'first_name',
             'last_name',
             'about_me'
         )}),
        ('Телеграм уведомления',
         {'fields': (
             'telegram_username',
             'telegram_notifications'
         )}),
        ('Изображение',
         {'fields': (
             'preview_image',
             'image'
         )}),
        ('Права доступа',
         {'fields': (
             'is_admin',
             'is_staff',
             'is_superuser',
             'is_email_verified'
         )}),
        ('Даты',
         {'fields': (
             'created_at',
             'last_login',
             'password_updated_at'
         )})
    )
    add_fieldsets = (
        (None,
         {'fields': (
             'slug',
             'email',
             'first_name',
             'last_name',
             'password1',
             'password2',
             'telegram_username',
             'image'
         )}),
    )
    ordering = ()
    filter_horizontal = ()
    list_filter = ()

    def preview_image(self, img):
        return mark_safe(
            f'<img src="{img.image.url}" style="height: 10rem;">')
