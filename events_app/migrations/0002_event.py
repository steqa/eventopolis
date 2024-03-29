# Generated by Django 4.2 on 2023-10-11 13:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('description', models.TextField(max_length=3000, verbose_name='описание')),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(90.0)], verbose_name='широта')),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(180.0)], verbose_name='долгота')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.eventcategory', verbose_name='категория')),
                ('members', models.ManyToManyField(related_name='участники', to=settings.AUTH_USER_MODEL, verbose_name='участники')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='организатор')),
            ],
            options={
                'verbose_name': 'мероприятие',
                'verbose_name_plural': 'мероприятия',
            },
        ),
    ]
