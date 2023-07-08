import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .decorators import unauthenticated_user
from .forms import CustomUserCreationForm
from .models import User
from .tokens import activation_token
from .utils import get_user_by_uid, send_activation_email, \
    send_reset_password_email


@unauthenticated_user
def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            return JsonResponse(data={'url': reverse('activation')}, status=302)
        else:
            return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

    return render(request, 'authentication/registration.html')


@unauthenticated_user
def activation(request):
    return render(request, 'authentication/activation.html')


@unauthenticated_user
def activate_user(request, uid: str, token: str):
    user = get_user_by_uid(uid)
    if user and activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'authentication/activation_fail.html', status=400)


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse(data={'url': '#'}, status=302)
        else:
            response = {'email': [
                {'message': 'Неверный адрес электронной почты или пароль.'}]}
            return JsonResponse(data=json.dumps(response), status=400, safe=False)

    return render(request, 'authentication/login.html')


@unauthenticated_user
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            send_reset_password_email(request, user.first())
            return JsonResponse(data={'url': reverse('activation')}, status=302)
        else:
            response = {'email': [
                {'message': 'Неверный адрес электронной почты.'}]}
            return JsonResponse(data=json.dumps(response), status=400, safe=False)
    return render(request, 'authentication/reset_password.html')


@unauthenticated_user
def reset_password_confirm(request, uid: str, token: str):
    user = get_user_by_uid(uid)
    if user and activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(data={'url': reverse('login')}, status=302)
            else:
                return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

        return render(request, 'authentication/reset_password_confirm.html')
    else:
        return render(request, 'authentication/activation_fail.html', status=400)
