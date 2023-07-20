from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from authentication.forms import CustomUserChangePersonalDataForm


def user_settings_personal(request):
    if request.method == 'POST':
        form = CustomUserChangePersonalDataForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse(data={'url': reverse('user-settings-personal')}, status=302)
        else:
            return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

    return render(request, 'user_profile/user_settings/personal.html')


def user_settings_security(request):
    return render(request, 'user_profile/user_settings/security.html')


def user_settings_notifications(request):
    return render(request, 'user_profile/user_settings/notifications.html')
