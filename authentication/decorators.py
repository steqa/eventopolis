from django.shortcuts import redirect


def unauthenticated_user(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('events')
        else:
            return func(request, *args, **kwargs)

    return wrapper_func
