from rest_framework import filters, viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsModerator)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserCreateView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = ()


class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model()
    serializer_class = UserSerializer
