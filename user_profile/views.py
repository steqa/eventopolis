from django.contrib.auth import logout
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from authentication.forms import UserEmailChangeForm, \
    UserPersonalDataChangeForm, UserSlugChangeForm
from authentication.tokens import activation_token
from authentication.utils import decode_urlsafe_base64, get_user_by_uid, \
    send_change_email_email


def user_settings_personal(request):
    if request.method == 'POST':
        form = UserPersonalDataChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse(data={'url': reverse('user-settings-personal')}, status=302)
        else:
            return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

    return render(request, 'user_profile/user_settings/personal.html')


def user_settings_security(request):
    if request.method == 'POST':
        field_type = request.GET.get('fieldType') if request.GET.get('fieldType') else None
        if field_type == 'slug':
            form = UserSlugChangeForm(request.POST)
            if form.is_valid():
                user = request.user
                user.slug = request.POST.get('slug')
                user.save()
                return JsonResponse(data={'url': reverse('user-settings-security')}, status=302)
            else:
                return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

    return render(request, 'user_profile/user_settings/security.html')


def user_settings_notifications(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'user_profile/user_settings/notifications.html')


def change_email(request):
    if request.method == 'POST':
        form = UserEmailChangeForm(request.user, request.POST)
        if form.is_valid():
            send_change_email_email(request, request.user,
                                    form.cleaned_data.get('new_email1'))
            return JsonResponse(
                data={'url': reverse('change-email-request-confirmation')}, status=302)
        else:
            return JsonResponse(
                data=form.errors.as_json(), status=400, safe=False)

    return render(request, 'user_profile/user_settings/change_email.html')


def change_email_request_confirmation(request):
    return render(request, 'user_profile/user_settings/change_email_request_confirmation.html')


def change_email_confirm(request, uid: str, token: str, new_email: str):
    user = get_user_by_uid(uid)
    if user and activation_token.check_token(user, token):
        new_email_decoded = decode_urlsafe_base64(new_email)
        user.email = new_email_decoded
        user.save()
        logout(request)
        return render(request, 'user_profile/user_settings/change_email_confirm.html')
    else:
        return render(request, 'authentication/activation_fail.html', status=400)