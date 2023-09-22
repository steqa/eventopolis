import json
import os
import shutil
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from authentication.models import User


class BaseTestCase(TestCase):
    login_url = settings.LOGIN_URL

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=0,
            email='test@gmail.com',
            first_name='First',
            last_name='Last',
            password='test1pass123',
            is_email_verified=True
        )
        cls.user.set_password('test1pass123')
        cls.user.save()
        cls.unauthorized_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)


class UserSettingsPersonal(BaseTestCase):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'user_images/0/')

    def image_dir_cleanup(self):
        shutil.rmtree(self.image_dir)

    user_settings_personal_url = reverse('user-settings-personal')

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.user_settings_personal_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_personal_url}'
        )

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.user_settings_personal_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/user_settings/personal.html')

    def test_POST_unauthorized(self):
        response = self.unauthorized_client.post(self.user_settings_personal_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_personal_url}'
        )

    def test_POST_authorized_no_data(self):
        response = self.authorized_client.post(self.user_settings_personal_url)

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized(self):
        response = self.authorized_client.post(self.user_settings_personal_url, {
            'first_name': 'FirstUpdated',
            'last_name': 'LastUpdated',
        })
        redirect_url = json.loads(response.content)['url']

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, self.user_settings_personal_url)
        self.assertEqual(User.objects.get(email='test@gmail.com').first_name, 'FirstUpdated')
        self.assertEqual(User.objects.get(email='test@gmail.com').last_name, 'LastUpdated')

    def test_POST_authorized_invalid_image(self):
        response = self.authorized_client.post(
            self.user_settings_personal_url + '?fieldType=image',
            {'attachment': get_test_image(size=(8200, 8200), img_format='PNG')}
        )

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized_valid_image(self):
        response = self.authorized_client.post(
            self.user_settings_personal_url + '?fieldType=image',
            {'image': get_test_image()}
        )
        redirect_url = json.loads(response.content)['url']

        self.addCleanup(self.image_dir_cleanup)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, self.user_settings_personal_url)


class UserSettingsSecurity(BaseTestCase):
    user_settings_security_url = reverse('user-settings-security')
    login_url = reverse('login')

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.user_settings_security_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_security_url}'
        )

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.user_settings_security_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/user_settings/security.html')

    def test_POST_unauthorized(self):
        response = self.unauthorized_client.post(self.user_settings_security_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_security_url}'
        )

    def test_POST_authorized_no_data(self):
        response = self.authorized_client.post(self.user_settings_security_url)

        self.assertEqual(response.status_code, 200)

    def test_POST_authorized_invalid_slug(self):
        response = self.authorized_client.post(
            self.user_settings_security_url + '?fieldType=slug',
            {'slug': '$invalid-slug$'}
        )

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized_valid_slug(self):
        response = self.authorized_client.post(
            self.user_settings_security_url + '?fieldType=slug',
            {'slug': 'valid_slug-5'})
        redirect_url = json.loads(response.content)['url']

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, self.user_settings_security_url)
        self.assertEqual(User.objects.get(email='test@gmail.com').slug, 'valid_slug-5')

    def test_POST_authorized_invalid_password(self):
        response = self.authorized_client.post(
            self.user_settings_security_url + '?fieldType=password',
            {'old_password': 'test1pass123',
             'new_password1': 'password',
             'new_password2': 'password'}
        )

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized_valid_password(self):
        response = self.authorized_client.post(
            self.user_settings_security_url + '?fieldType=password',
            {'old_password': 'test1pass123',
             'new_password1': 'test1pass123_new',
             'new_password2': 'test1pass123_new'}    
        )
        redirect_url = json.loads(response.content)['url']

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, self.login_url)


class UserSettingsNotifications(BaseTestCase):
    user_settings_notifications_url = reverse('user-settings-notifications')

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.user_settings_notifications_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_notifications_url}'
        )

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.user_settings_notifications_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/user_settings/notifications.html')
        self.assertEqual(response.context.get('telegram_bot_url'), settings.TELEGRAM_BOT_URL)

    def test_POST_unauthorized(self):
        response = self.unauthorized_client.post(self.user_settings_notifications_url)

        self.assertRedirects(
            response, self.login_url + f'?next={self.user_settings_notifications_url}'
        )

    def test_POST_authorized_no_data(self):
        response = self.authorized_client.post(self.user_settings_notifications_url)

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized_invalid_data(self):
        response = self.authorized_client.post(self.user_settings_notifications_url, {
            'telegram_username': 'invalid-username',
        })

        self.assertEqual(response.status_code, 400)

    def test_POST_authorized_valid_data(self):
        response = self.authorized_client.post(self.user_settings_notifications_url, {
            'telegram_username': 'valid_username',
        })
        redirect_url = json.loads(response.content)['url']

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, self.user_settings_notifications_url)
        self.assertEqual(User.objects.get(email='test@gmail.com').telegram_username, 'valid_username')


def get_test_image(size=(8150, 8150), img_format='JPEG'):
    image = Image.new(mode='RGB', size=size, color='white')
    buffer = BytesIO()
    image.save(buffer, format=img_format, quality=100)
    buffer.seek(0)
    test_image = SimpleUploadedFile(f'test_image.{img_format.lower()}', buffer.read())
    buffer.close()
    return test_image
