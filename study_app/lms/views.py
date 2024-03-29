from rest_framework import generics, viewsets
from rest_framework.views import APIView
from users.models import UserRoles
from users.permissions import IsOwner, IsModerator
from lms.models.models import Course, Lesson
from lms.models.subscription import Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from .paginators import CoursePagination, LessonPagination


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    pagination_class = LessonPagination

    serializer_class = LessonSerializer

    def get(self, request):
        pagination_queryset = self.paginate_queryset(self.queryset)
        serializer_class = LessonSerializer(pagination_queryset, many=True)
        return self.get_paginated_response(serializer_class.data)

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user) if self.request.user.role == UserRoles.MEMBER else super().get_queryset()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonDetailView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, *args, **kwargs):

        course = Course.objects.get(pk=self.kwargs['pk'])

        user = self.request.user
        subscription = Subscription.objects.filter(course=course,
                                                   owner=user).first()

        if subscription.status:
            subscription.status = False
            subscription.save()
            message = 'Вы отписались от курса.'
        else:
            subscription.status = True
            subscription.save()
            message = 'Вы подписались на курс.'

        return Response({"message": message})
