from django.http.response import JsonResponse
from django.shortcuts import render

from .forms import CustomUserCreationForm


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            ...
        else:
            return JsonResponse(
                data=form.errors.as_json(),
                status=400, safe=False)

    return render(request, 'account/registration.html')
