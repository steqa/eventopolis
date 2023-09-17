from django.test import TestCase

from authentication.forms import (CustomUserCreationForm, UserEmailChangeForm,
                                  UserPersonalDataChangeForm)
from authentication.models import User


class CustomUserCreationFormTestCase(TestCase):
    def test_valid_data(self):
        form = CustomUserCreationForm(data={
            'email': 'test@gmail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'test1pass123',
            'password2': 'test1pass123'
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = CustomUserCreationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_name_in_lower_case(self):
        form = CustomUserCreationForm(data={
            'email': 'test@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password1': 'test1pass123',
            'password2': 'test1pass123'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class UserPersonalDataChangeFormTestCase(TestCase):
    def test_valid_data(self):
        form = UserPersonalDataChangeForm(data={
            'first_name': 'First',
            'last_name': 'Last',
            'about_me': 'About'
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = UserPersonalDataChangeForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class UserEmailChangeFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test@gmail.com',
            first_name='First',
            last_name='Last',
            password='test1pass123',
            is_email_verified=True
        )
        cls.second_user = User.objects.create(
            email='test_second@gmail.com',
            first_name='First',
            last_name='Last',
            password='test1pass123',
            is_email_verified=True
        )

    def test_valid_data(self):
        form = UserEmailChangeForm(self.user, data={
            'new_email1': 'test_valid_data@gmail.com',
            'new_email2': 'test_valid_data@gmail.com'
        })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = UserEmailChangeForm(self.user, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_email_mismatch(self):
        form = UserEmailChangeForm(self.user, data={
            'new_email1': 'test_email@gmail.com',
            'new_email2': 'test_email_mismatch@gmail.com'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_not_changed(self):
        form = UserEmailChangeForm(self.user, data={
            'new_email1': 'test@gmail.com',
            'new_email2': 'test@gmail.com'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_email_exists(self):
        form = UserEmailChangeForm(self.user, data={
            'new_email1': 'test_second@gmail.com',
            'new_email2': 'test_second@gmail.com'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
