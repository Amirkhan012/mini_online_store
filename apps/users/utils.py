from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)


def send_activation_email(user, request):
    """
    Отправляет активационное письмо указанному пользователю.

    Эта функция генерирует уникальный токен и идентификатор пользователя,
    создает ссылку для активации и отправляет письмо пользователю со
    ссылкой для активации его аккаунта.
    """
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = request.build_absolute_uri(reverse(
            'verify-email',
            kwargs={'uid': uid, 'token': token})
        )
        subject = 'Activate your account'
        message = render_to_string('users/activate_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject, message, from_email, [user.email], html_message=message
        )
        logger.info(f"Activation email sent to {user.email}")
    except Exception as e:
        logger.error(f"Error sending activation email: {e}")
