from django.urls import path

from . import views

urlpatterns = [
    path('settings/personal',
         views.user_settings_personal,
         name='user-settings-personal'),
    path('settings/security',
         views.user_settings_security,
         name='user-settings-security'),
    path('settings/notifications',
         views.user_settings_notifications,
         name='user-settings-notifications'),
]
