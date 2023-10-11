from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


def _get_image_filepath(self, image_name: str) -> str:
    return f'user_images/{self.event.owner.pk}/{self.event.pk}/{image_name}'


class Event(models.Model):
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='организатор',
        on_delete=models.CASCADE
    )
    members = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        verbose_name='участники',
        related_name='участники'
    )
    name = models.CharField(
        verbose_name='название',
        max_length=50
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=3000
    )
    category = models.ForeignKey(
        to='EventCategory',
        verbose_name='категория',
        on_delete=models.CASCADE
    )
    latitude = models.FloatField(
        verbose_name='широта',
        validators=[MinValueValidator(0.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        verbose_name='долгота',
        validators=[MinValueValidator(0.0), MaxValueValidator(180.0)]
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
    
    def __str__(self) -> str:
        return self.name


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


class EventImage(models.Model):
    event = models.ForeignKey(
        to='Event',
        verbose_name='мероприятие',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to=_get_image_filepath
    )
    
    class Meta:
        verbose_name = 'изображение мероприятия'
        verbose_name_plural = 'изображения мероприятий'
    
    def __str__(self):
        return self.image.name.split('/')[-1]
