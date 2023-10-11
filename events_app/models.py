from django.db import models


class EventCategory(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=50
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'категория мероприятия'
        verbose_name_plural = 'категории мероприятий'

    def __str__(self) -> str:
        return self.name
