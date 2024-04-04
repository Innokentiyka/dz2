from rest_framework import filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwnerOrStaff
from users.models import CustomUser
from rest_framework.response import Response

from .services import create_stripe_price, create_stripe_session


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        password = serializer.data["password"]
        user = CustomUser.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model()
    serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
    """
    Класс для формирования списка платежей
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    search_fields = ['paid_lesson', 'paid_course', 'method_payment']
    ordering_fields = ('date_of_payment',)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('user', 'date_of_payment',
                        'paid_lesson', 'paid_course')
    filter_fields = ('user', 'date_of_payment',
                     'paid_lesson', 'paid_course')
    permission_classes = [IsOwnerOrStaff]


class PaymentCreateView(generics.CreateAPIView):
    """
    Класс для создания нового платежа
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        payment = serializer.save()
        stripe_price_id = create_stripe_price(payment)
        payment.payment_url, payment.payment_id = (
            create_stripe_session(stripe_price_id)
        )
        payment.save()


class PaymentDetailView(generics.RetrieveAPIView):
    """
    Класс для просмотра подробной информации по платежу
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]


class PaymentUpdateView(generics.UpdateAPIView):
    """
    Класс для обновления данных по платежу
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]


class PaymentDestroyView(generics.DestroyAPIView):
    """
    Класс для удаления платежа
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]
