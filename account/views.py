import json

from django.contrib.auth import authenticate, login
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
            return JsonResponse(data={'url': reverse('activation')}, status=302)
        else:
            return JsonResponse(data=form.errors.as_json(), status=400, safe=False)

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
        return redirect('login')
    else:
        return render(request, 'account/activation_fail.html', status=400)


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

    return render(request, 'account/login.html')
