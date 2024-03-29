from lms.models.models import Lesson, Course
from lms.models.subscription import Subscription
from rest_framework import serializers

from .validators import VideoValidators


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'preview', 'owner',
                  'description', 'video_url', 'course']
        validators = [
            VideoValidators(field='video_url'),

        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'owner', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'owner', 'course', 'status']
