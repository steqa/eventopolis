from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .decorators import unauthenticated_user
from .forms import CustomUserCreationForm
from .tokens import activation_token
from .utils import get_user_by_uid
from .utils import send_activation_email


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
