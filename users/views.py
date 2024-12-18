from rest_framework import generics

from users.models import User
from users.serializers import UserCreateSerializer, UserUpdateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
