from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activation/', views.activation, name='activation'),
    path('activation/<uid>/<token>', views.activate_user, name='activate-user'),
    path('login/', views.login_user, name='login'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('reset-password/confirm/<uid>/<token>',
         views.reset_password_confirm, name='reset-password-confirm')
]
