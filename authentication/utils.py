from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from authentication.models import User

from .thread import SendEmailThread
from .tokens import activation_token


def send_activation_email(request, user: User) -> None:
    subject = 'Eventopolis: подтвердите регистрацию.'
    body = render_to_string('authentication/activation_email.html', {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user)
    })
    send_email(to_email=user.email, subject=subject, body=body)


def send_reset_password_email(request, user: User) -> None:
    subject = 'Eventopolis: восстановление пароля.'
    body = render_to_string('authentication/reset_password_email.html', {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user)
    })
    send_email(to_email=user.email, subject=subject, body=body)


def send_change_email_email(request, user: User, new_email: str) -> None:
    subject = 'Eventopolis: изменение адреса электронной почты.'
    body = render_to_string('user_profile/user_settings/change_email_email.html', {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
        'new_email': urlsafe_base64_encode(force_bytes(new_email))
    })
    send_email(to_email=new_email, subject=subject, body=body)


def send_email(to_email: str, subject: str, body: str) -> None:
    email = EmailMessage(subject=subject, body=body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[to_email])
    SendEmailThread(email).start()


def get_user_by_uid(uid: str) -> User | None:
    try:
        user_pk = decode_urlsafe_base64(uid)
        user = User.objects.get(pk=user_pk)
    except:
        user = None

    return user


def decode_urlsafe_base64(string: str):
    return force_str(urlsafe_base64_decode(string))
