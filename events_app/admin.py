from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Event, EventCategory, EventImage



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'category', 'latitude', 'longitude')
    search_fields = ('owner', 'name', 'category')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        (None,
         {'fields': (
             'id',
             'owner',
             'members',
         )}),
        ('Описание',
         {'fields': (
             'name',
             'description',
             'category'
         )}),
        ('Местоположение',
         {'fields': (
             'latitude',
             'longitude'
         )}),
        ('Даты',
         {'fields': (
             'created_at',
         )})
    )


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        (None,
         {'fields': (
             'id',
         )}),
        ('Описание',
         {'fields': (
             'name',
         )}),
        ('Даты',
         {'fields': (
             'created_at',
         )})
    )


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image_preview')
    readonly_fields = ('id', 'image_preview_inside')
    fieldsets = (
        (None,
         {'fields': (
             'id',
             'event',
         )}),
        ('Изображение',
         {'fields': (
             'image',
             'image_preview_inside',
         )}),
    )

    def image_preview(self, event: Event):
        if event.image:
            return mark_safe(f'<img src="{event.image.url}" style="max-height: 25px;">')
        else:
            return 'Отсутствует'

    image_preview.short_description = 'изображение'

    def image_preview_inside(self, event: Event):
        if event.image:
            return mark_safe(f'<img src="{event.image.url}" style="max-height: 200px;">')
        else:
            return 'Отсутствует'

    image_preview_inside.short_description = 'просмотр изображения'
