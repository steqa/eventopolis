from django.shortcuts import render


def user_settings_personal(request):
    return render(request, 'user_profile/user_settings/personal.html')


def user_settings_security(request):
    return render(request, 'user_profile/user_settings/security.html')


def user_settings_notifications(request):
    return render(request, 'user_profile/user_settings/notifications.html')
