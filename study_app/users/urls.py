from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserUpdateDeleteView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:pk>/', UserUpdateDeleteView.as_view()),
]
