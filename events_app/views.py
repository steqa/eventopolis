from django.shortcuts import render


def events(request):
    return render(request, 'events_app/events.html')
