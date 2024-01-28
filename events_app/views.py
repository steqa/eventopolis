from django.shortcuts import render
from . models import Event, EventImage, EventCategory


def events(request):
    events = Event.objects.all()
    event_images = EventImage.objects.all()
    categories = EventCategory.objects.all()
    
    images_by_event_id = {}
    for image in event_images:
        if image.event.id in images_by_event_id:
            images_by_event_id[image.event.id].append(image)
        else:
             images_by_event_id[image.event.id] = [image]

    context = {
        'events': events,
        'images': images_by_event_id,
        'categories': categories
    }
    return render(request, 'events_app/events.html', context)
