import os
import shutil
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from authentication.models import User


class TestModels(TestCase):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'user_images/0/')

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

    def test_default_path_to_the_profile_image_is_set_correctly(self):
        expected_filepath = os.path.join(settings.MEDIA_ROOT, 'default_profile_image.jpg')

        self.assertEqual(self.user.image.path, expected_filepath)

    def test_path_to_the_profile_image_is_set_correctly(self):
        self.user.image = get_test_image()
        self.user.save()

        self.addCleanup(self.image_dir_cleanup)
        self.assertEqual(self.user.image.path, self.image_dir + 'profile_image.jpg')

    def test_save(self):
        # first_name and last_name lower case
        with self.assertRaises(ValidationError) as error:
            create_user(first_name='first', last_name='last')
        self.assertEqual(len(error.exception.message_dict), 2)

        # first_name and last_name the letters only
        with self.assertRaises(ValidationError) as error:
            create_user(first_name='0', last_name='0')
        self.assertEqual(len(error.exception.message_dict), 2)

        # telegram_username
        with self.assertRaises(ValidationError) as error:
            create_user(telegram_username='`~!@#$%^&*()-=+"№;:?<>{}[]/\\.,')
        self.assertEqual(len(error.exception.message_dict), 1)

        # image
        with self.assertRaises(ValidationError) as error:
            test_image = get_test_image(size=(8200, 8200))
            create_user(image=test_image)
        self.assertEqual(len(error.exception.message_dict), 1)

        with self.assertRaises(ValidationError) as error:
            test_image = get_test_image(img_format='PNG')
            create_user(image=test_image)
        self.assertEqual(len(error.exception.message_dict), 1)

        # slug
        with self.assertRaises(ValidationError) as error:
            create_user(slug=self.user.slug)
        self.assertEqual(len(error.exception.message_dict), 1)


def create_user(
        email='testemail@gmail.com',
        first_name='First',
        last_name='Last',
        telegram_username=None,
        image=os.path.basename('default_profile_image.jpg'),
        slug=None,
        is_email_verified=True,
        password='test1pass123'
):
    User.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        telegram_username=telegram_username,
        image=image,
        slug=slug,
        is_email_verified=is_email_verified,
        password=password
    )


def get_test_image(size=(8150, 8150), img_format='JPEG'):
    image = Image.new(mode='RGB', size=size, color='white')
    buffer = BytesIO()
    image.save(buffer, format=img_format, quality=100)
    buffer.seek(0)
    test_image = SimpleUploadedFile(f'test_image.{img_format.lower()}', buffer.read())
    buffer.close()
    return test_image
