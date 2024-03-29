from django.db import models
from django.conf import settings


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses_previews/', blank=True, null=True)
    description: str = models.TextField()

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('title',)


class Lesson(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    preview = models.ImageField(upload_to='lessons_previews/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('title', 'course',)
