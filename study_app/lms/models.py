from django.db import models


class Course(models.Model):
    title: str = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses_previews/', blank=True, null=True)
    description: str = models.TextField()


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    preview = models.ImageField(upload_to='lessons_previews/', blank=True, null=True)
    video_url = models.URLField()
