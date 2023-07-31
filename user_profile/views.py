from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render

from authentication.forms import UserEmailChangeForm, \
    UserPersonalDataChangeForm, UserSlugChangeForm
from authentication.tokens import activation_token
from authentication.utils import decode_urlsafe_base64, get_user_by_uid, \
    send_change_email_email
from eventopolis.utils import JsonFormErrorsResponse, JsonRedirectResponse


def user_settings_personal(request):
    if request.method == 'POST':
        user = request.user
        form = UserPersonalDataChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonRedirectResponse(url='user-settings-personal')
        else:
            return JsonFormErrorsResponse(form=form)

    return render(request, 'user_profile/user_settings/personal.html')


def user_settings_security(request):
    if request.method == 'POST':
        user = request.user
        field_type = request.GET.get('fieldType') if request.GET.get('fieldType') else None
        if field_type == 'slug':
            form = UserSlugChangeForm(request.POST)
            if form.is_valid():
                user.slug = request.POST.get('slug')
                user.save()
                return JsonRedirectResponse(url='user-settings-security')
            else:
                return JsonFormErrorsResponse(form=form)
        elif field_type == 'password':
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonRedirectResponse(url='login')
            else:
                return JsonFormErrorsResponse(form=form)

    return render(request, 'user_profile/user_settings/security.html')


def user_settings_notifications(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'user_profile/user_settings/notifications.html')


def change_email(request):
    if request.method == 'POST':
        form = UserEmailChangeForm(request.user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get('new_email1')
            send_change_email_email(
                request, user=request.user, new_email=new_email
            )
            return JsonRedirectResponse(url='change-email-request-confirmation')
        else:
            return JsonFormErrorsResponse(form=form)

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
