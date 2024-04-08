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

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    search_fields = ['lesson', 'course', 'method_payment']
    ordering_fields = ('payment_date',)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('user', 'payment_date',
                        'lesson', 'course')
    filter_fields = ('user', 'payment_date',
                     'lesson', 'course')
    permission_classes = [IsOwnerOrStaff]


class PaymentCreateView(generics.CreateAPIView):

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

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]


class PaymentUpdateView(generics.UpdateAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]


class PaymentDestroyView(generics.DestroyAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all
    permission_classes = [IsOwnerOrStaff]
