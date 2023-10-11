from django.contrib import admin

from .models import Event, EventCategory


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
