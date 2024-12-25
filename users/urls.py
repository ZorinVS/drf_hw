from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('users/create/', views.UserCreateAPIView.as_view(), name='users-create'),
    path('users/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='users-update'),
]
