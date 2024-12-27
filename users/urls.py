from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('users/create/', views.UserCreateAPIView.as_view(), name='users-create'),
    path('users/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='users-get'),
    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='users-update'),

    # Payment
    path('payments/create/', views.PaymentCreateAPIView.as_view(), name='payments-create'),
    path('payments/', views.PaymentListAPIView.as_view(), name='payments-list'),
]
