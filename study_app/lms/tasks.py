from celery import shared_task
from django.core.mail import send_mail

from lms.models.subscription import Subscription
from django.conf import settings


@shared_task
def send_email_for_update_course(course_id):
    subs = Subscription.objects.filter(course=course_id, status=True)
    for sub in subs:
        course = sub.course
        user = sub.owner
        send_mail(
            subject=f'{course} обновился',
            message=f'{course} обновился, скорее посмотрите изменения!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
