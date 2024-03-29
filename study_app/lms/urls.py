from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListView, LessonDestroyView, LessonCreateView, LessonDetailView, \
    LessonUpdateView, SubscriptionAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateView.as_view(),
         name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(),
         name='lesson_delete'),
    path('courses/<int:pk>/subscription/', SubscriptionAPIView.as_view(),
         name='subscription')
]
