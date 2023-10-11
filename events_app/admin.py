from django.contrib import admin

from .models import EventCategory


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
