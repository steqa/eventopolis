from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .decorators import unauthenticated_user
from .forms import CustomUserCreationForm
from .tokens import activation_token
from .utils import get_user_by_uid, send_activation_email


@unauthenticated_user
def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            return JsonResponse(
                data={
                    'redirect': request.build_absolute_uri(reverse('activation'))
                },
                status=200)
        else:
            return JsonResponse(
                data=form.errors.as_json(),
                status=400, safe=False)

    return render(request, 'account/registration.html')


@unauthenticated_user
def activation(request):
    return render(request, 'account/activation.html')


@unauthenticated_user
def activate_user(request, uid: str, token: str):
    user = get_user_by_uid(uid)
    if user and activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect('registration')
    else:
        return render(request, 'account/activation_fail.html')
