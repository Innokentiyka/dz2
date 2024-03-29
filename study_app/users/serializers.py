from .models import Payment
from rest_framework import serializers
from django.contrib.auth import get_user_model


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password', 'phone', 'city', 'avatar')



