from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import User
from .thread import SendEmailThread
from .tokens import activation_token


def send_activation_email(request, user: User) -> None:
    subject = 'Eventopolis: подтвердите регистрацию.'
    body = render_to_string('account/activation_email.html', {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user)
    })
    send_email(user, subject, body)


def send_email(user: User, subject: str, body: str) -> None:
    email = EmailMessage(subject=subject, body=body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email])
    SendEmailThread(email).start()
