from django.urls import path
from .views import UserUpdateDeleteView, PaymentListView, PaymentCreateView, PaymentDetailView, \
    PaymentUpdateView, PaymentDestroyView

urlpatterns = [

    path('user/<int:pk>/', UserUpdateDeleteView.as_view()),
    path('payment/', PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateView.as_view(),
         name='payment_create'),
    path('payment/detail/<int:pk>/', PaymentDetailView.as_view(),
         name='payment_detail'),
    path('payment/update/<int:pk>/', PaymentUpdateView.as_view(),
         name='payment_update'),
    path('payment/delete/<int:pk>/', PaymentDestroyView.as_view(),
         name='payment_delete'),
]
