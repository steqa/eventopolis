from django.urls import path

from . import views

urlpatterns = [
    path('settings/personal/',
         views.user_settings_personal,
         name='user-settings-personal'),
    path('settings/security/',
         views.user_settings_security,
         name='user-settings-security'),
    path('settings/notifications/',
         views.user_settings_notifications,
         name='user-settings-notifications'),
    path('settings/change-email/',
         views.change_email,
         name='change-email'),
    path('settings/change-email/confirm/',
         views.change_email_request_confirmation,
         name='change-email-request-confirmation'),
    path('settings/change-email/confirm/<uid>/<token>/<new_email>/',
         views.change_email_confirm,
         name='change-email-confirm'),
]
