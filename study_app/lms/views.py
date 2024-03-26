from rest_framework import generics, viewsets

from users.permissions import IsOwner, IsModerator
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


class LessonListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, ~IsModerator)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
