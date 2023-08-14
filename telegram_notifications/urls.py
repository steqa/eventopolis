from django.urls import path

from . import views

urlpatterns = [
    path('enable-telegram-bot/',
         views.enable_telegram_bot,
         name='enable-telegram-bot'),
    path('disable-telegram-bot/',
         views.disable_telegram_bot,
         name='disable-telegram-bot')
]
