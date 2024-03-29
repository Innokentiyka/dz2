from django.contrib import admin
from lms.models.models import Course, Lesson
from lms.models.subscription import Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'preview']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'description', 'preview', 'video_url']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'course', 'status',)
    list_filter = ('owner', 'course', 'status',)
