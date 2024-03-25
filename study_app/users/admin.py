from django.contrib import admin
from .models import CustomUser, Payment


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'city', 'avatar']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
