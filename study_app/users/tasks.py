from celery import shared_task
import datetime

from users.models import CustomUser


@shared_task
def check_user_activity():

    users = CustomUser.objects.all()
    date_now = datetime.date.today()
    deactivate_time = datetime.timedelta(days=30)
    for user in users:
        if date_now - user.last_login > deactivate_time:
            user.is_active = False
            user.save()