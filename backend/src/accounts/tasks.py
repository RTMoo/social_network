from random import randint
from celery import shared_task
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings


@shared_task
def send_confirmation_email(email):
    code = str(randint(100000, 999999))

    send_mail(
        subject="Ваш код подтверждения",
        message=f"Ваш код подтверждения: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    cache.set(email, code, 300)
