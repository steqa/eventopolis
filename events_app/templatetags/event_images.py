from django import template

register = template.Library()


@register.filter(name='get_event_images')
def get_event_images(dictionary: dict, key: int) -> list:
    return dictionary[key]


@register.filter(name='get_first_event_image_url')
def get_first_event_image_url(dictionary: dict, key: int) -> str:
    return dictionary[key][0].image.url