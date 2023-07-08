import os
import shutil
import tempfile

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from authentication.models import User


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            pk=0,
            email='test@gmail.com',
            first_name='First',
            last_name='Last',
            password='test1pass123',
            is_email_verified=True
        )

    def test_default_path_to_the_profile_image_is_set_correctly(self):
        expected_filepath = os.path.join(settings.MEDIA_ROOT, 'default_profile_image.jpg')

        self.assertEqual(self.user.image.path, expected_filepath)

    def test_path_to_the_profile_image_is_set_correctly(self):
        image_dir = os.path.join(settings.MEDIA_ROOT, 'user_images/0/')

        def cleanup():
            shutil.rmtree(image_dir)

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            self.user.image = SimpleUploadedFile(tmp_file.name, tmp_file.read())
            self.user.save()

        self.addCleanup(cleanup)
        self.assertEqual(self.user.image.path, image_dir + 'profile_image.jpg')

    def test_save(self):
        expected_error_messages = {
            'first_name': ['Имя не должно начинаться с маленькой буквы.'],
            'last_name': ['Фамилия не должна начинаться с маленькой буквы.']
        }
        with self.assertRaises(ValidationError) as error:
            User.objects.create(
                email='test2@gmail.com',
                first_name='first',
                last_name='last',
                password='test1pass123',
                is_email_verified=True
            )

        self.assertEqual(error.exception.message_dict, expected_error_messages)
