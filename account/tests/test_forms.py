from django.test import TestCase

from account.forms import CustomUserCreationForm


class TestForms(TestCase):
    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(data={
            'email': 'test@gmail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'test1pass123',
            'password2': 'test1pass123'
        })

        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_no_data(self):
        form = CustomUserCreationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_custom_user_creation_form_name_in_lower_case(self):
        form = CustomUserCreationForm(data={
            'email': 'test@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password1': 'test1pass123',
            'password2': 'test1pass123'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
