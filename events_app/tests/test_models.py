import os
import shutil
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from authentication.models import User
from events_app.models import Event, EventCategory, EventImage


class TestEventImageModel(TestCase):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'user_images/0/0/')

    def image_dir_cleanup(self):
        shutil.rmtree(self.image_dir)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            pk=0,
            email='test@gmail.com',
            first_name='First',
            last_name='Last',
            is_email_verified=True,
            password='test1pass123'
        )
        cls.event_category = EventCategory.objects.create(
            pk=0,
            name='Name'
        )
        cls.event = Event.objects.create(
            pk=0,
            owner=cls.user,
            name='Name',
            description='Description',
            category=cls.event_category,
            latitude=0,
            longitude=100
        )

    def test_path_to_the_event_image_is_set_correctly(self):
        image = get_test_image()
        event_image = EventImage.objects.create(
            event=self.event,
            image=image
        )

        self.addCleanup(self.image_dir_cleanup)
        self.assertEqual(
            event_image.image.path,
            self.image_dir + image.name
        )
    
    def test_save(self):
        with self.assertRaises(ValidationError) as error:
            EventImage.objects.create(
                event=self.event,
                image=get_test_image(size=(8200, 8200))
            )
        self.assertEqual(len(error.exception.message_dict), 1)

        with self.assertRaises(ValidationError) as error:
            EventImage.objects.create(
                event=self.event,
                image=get_test_image(img_format='PNG')
            )
        self.assertEqual(len(error.exception.message_dict), 1)


def get_test_image(size=(8150, 8150), img_format='JPEG'):
    image = Image.new(mode='RGB', size=size, color='white')
    buffer = BytesIO()
    image.save(buffer, format=img_format, quality=100)
    buffer.seek(0)
    test_image = SimpleUploadedFile(f'test_image.{img_format.lower()}', buffer.read())
    buffer.close()
    return test_image
