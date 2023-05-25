from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activation/', views.activation, name='activation'),
    path('activation/<uid>/<token>', views.activate_user, name='activate-user'),
]
