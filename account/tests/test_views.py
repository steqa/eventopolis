import json
import threading

from django.test import Client, TestCase
from django.urls import reverse

from account.models import User
from account.thread import SendEmailThread


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@gmail.com',
            first_name='First',
            last_name='Last',
            password='test1pass123',
            is_email_verified=True
        )
        cls.unauthorized_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)


class RegistrationTestCase(BaseTestCase):
    registration_url = reverse('registration')
    login_user_url = reverse('login')

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.registration_url)

        self.assertRedirects(response, reverse('events'))

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.registration_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/registration.html')

    def test_POST_authorized(self):
        response = self.authorized_client.post(self.registration_url)

        self.assertRedirects(response, reverse('events'))

    def test_POST_unauthorized_no_data(self):
        response = self.unauthorized_client.post(self.registration_url)

        self.assertEqual(response.status_code, 400)

    def test_POST_unauthorized_and_activate_user(self):
        response = self.unauthorized_client.post(self.registration_url, {
            'email': 'test2@gmail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'test1pass123',
            'password2': 'test1pass123'
        })
        redirect_url = json.loads(response.content)['url']
        try:
            thread = threading.enumerate()[1]
        except IndexError:
            thread = None

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url, reverse('activation'))
        self.assertTrue(User.objects.filter(email='test2@gmail.com').exists())
        self.assertFalse(User.objects.get(email='test2@gmail.com').is_email_verified)
        self.assertIsInstance(thread, SendEmailThread)

        email = thread.__dict__['email'].__dict__
        activation_token = email['body'].split('\n')[4].split('/')[-1]
        uid = email['body'].split('\n')[4].split('/')[-2]
        email_to = email['to'][0]

        self.assertEqual(email_to, 'test2@gmail.com')

        response = self.unauthorized_client.get(reverse('activate-user', kwargs={
            'uid': uid,
            'token': activation_token
        }))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_user_url)
        self.assertTrue(User.objects.get(email='test2@gmail.com').is_email_verified)


class ActivationTestCase(BaseTestCase):
    activation_url = reverse('activation')

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.activation_url)

        self.assertRedirects(response, reverse('events'))

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.activation_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/activation.html')


class ActivateUserTestCase(BaseTestCase):

    def test_GET_authorized(self):
        response = self.authorized_client.get(reverse('activate-user', kwargs={
            'uid': None,
            'token': None
        }))

        self.assertRedirects(response, reverse('events'))

    def test_GET_unauthorized_no_data(self):
        response = self.unauthorized_client.get(reverse('activate-user', kwargs={
            'uid': None,
            'token': None
        }))

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'account/activation_fail.html')


class LoginUserTestCase(BaseTestCase):
    login_user_url = reverse('login')

    def test_GET_authorized(self):
        response = self.authorized_client.get(self.login_user_url)

        self.assertRedirects(response, reverse('events'))

    def test_GET_unauthorized(self):
        response = self.unauthorized_client.get(self.login_user_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_POST_authorized(self):
        response = self.authorized_client.post(self.login_user_url)

        self.assertRedirects(response, reverse('events'))

    def test_POST_unauthorized_no_data(self):
        response = self.unauthorized_client.post(self.login_user_url)

        self.assertEqual(response.status_code, 400)

    def test_POST_unauthorized_invalid_data(self):
        response = self.unauthorized_client.post(self.login_user_url, {
            'email': 'test@gmail.com',
            'password': 'wrong-password'
        })

        self.assertEqual(response.status_code, 400)
