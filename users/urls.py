from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserCreateAPIView.as_view(), name='users-create'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='users-update'),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view(), name='users-delete'),
    path('', views.UserListAPIView.as_view(), name='users-list'),
    path('<int:pk>/', views.UserRetrieveAPIView.as_view(), name='users-get'),

    # Payment
    path('payments/create/', views.PaymentCreateAPIView.as_view(), name='payments-create'),
    path('payments/', views.PaymentListAPIView.as_view(), name='payments-list'),
]
