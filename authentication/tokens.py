import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def check_token(self, user, token):
        if super().check_token(user, token):
            ts = base36_to_int(token.split("-")[0])
            if (self._num_seconds(
                    self._now()) - ts) > settings.EMAIL_ACTIVATION_TIMEOUT:
                return False
            return True
        else:
            return False

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + \
            six.text_type(timestamp) + \
            six.text_type(user.is_email_verified)


activation_token = ActivationTokenGenerator()
