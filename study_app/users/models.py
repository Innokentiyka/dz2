from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from lms.models.models import Course, Lesson


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта пользователя')
    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['']

    role = models.CharField(max_length=9, choices=UserRoles.choices,
                            default=UserRoles.MEMBER)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=(('cash', 'Cash'), ('transfer', 'Transfer')))

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)

    payment_url = models.URLField(max_length=400, null=True, blank=True,
                                  verbose_name='ссылка на оплату')
    payment_id = models.CharField(max_length=100, null=True, blank=True,
                                  verbose_name='id платежа')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
