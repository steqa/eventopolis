# Generated by Django 4.2 on 2023-10-11 13:04

from django.db import migrations, models
import django.db.models.deletion
import events_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0002_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=events_app.models._get_image_filepath, verbose_name='изображение')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_app.event', verbose_name='мероприятие')),
            ],
            options={
                'verbose_name': 'изображение мероприятия',
                'verbose_name_plural': 'изображения мероприятий',
            },
        ),
    ]
