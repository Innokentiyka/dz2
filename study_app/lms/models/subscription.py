from users.models import CustomUser
from django.db import models
from .models import Course


class Subscription(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='владелец',
                              related_name='subscription')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name='курс',
                               related_name='subscriptions')
    status = models.BooleanField(default=False, verbose_name='статус подписки', blank=True, null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.owner}: {self.course} {self.id}'
